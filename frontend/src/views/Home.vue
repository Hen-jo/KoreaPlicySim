<template>
  <section class="seoul-page">
    <header class="hero">
      <p class="hero-eyebrow">서울 지도 기반 정당 성향 지도</p>
      <h1>구를 누르면, 그 동네의 성향이 펼쳐집니다.</h1>
      <p class="hero-copy">
        서울시 구경계를 실제 행정구역 GeoJSON으로 표시하고, 2024년 제21대 국회의원선거 구 단위 득표율(구성 정당 기준)로 색이 바뀝니다.
        구를 클릭하면 선거 지지도와 동네 인구/성별/연령 지표를 함께 확인할 수 있습니다.
      </p>
    </header>

    <section class="main-grid">
      <div class="map-shell">
        <div class="map-frame">
          <div class="map-lights"></div>
          <div class="map-shadow"></div>
          <div class="map-wrap" ref="mapWrap">
            <svg ref="mapSvg" class="seoul-map" viewBox="0 0 960 680" role="img" aria-label="서울시 구별 정당 성향 지도"></svg>
            <div v-if="loading" class="map-mask">
              <span>지도 로딩 중...</span>
            </div>
            <div v-if="error" class="map-mask map-mask--error">
              <span>{{ error }}</span>
            </div>
          </div>
        </div>

        <div class="legend-row" role="list">
          <button
            v-for="party in legendItems"
            :key="party.id"
            class="legend-pill"
            :class="{ active: activeParty === party.id }"
            @click="setPartyFilter(party.id)"
            :style="{ '--party-color': party.color }"
            role="button"
            :aria-label="`${party.name}만 강조`">
            <span>{{ party.name }}</span>
          </button>
        </div>
      </div>

      <aside class="detail-pane">
        <div class="detail-head">
          <p class="detail-kicker">서울 구석</p>
          <h2>{{ selectedDistrict?.properties.name || '구를 선택해 주세요' }}</h2>
        </div>

        <nav class="step-tabs" role="tablist" aria-label="시뮬레이션 단계">
          <button
            class="step-tab"
            :class="{ 'is-active': activeStep === 1 }"
            @click="setActiveStep(1)"
          >
            1. 정책 입력
          </button>
          <button
            class="step-tab"
            :class="{ 'is-active': activeStep === 2 }"
            @click="setActiveStep(2)"
          >
            2. 실행 · 추이
          </button>
          <button
            class="step-tab"
            :class="{ 'is-active': activeStep === 3 }"
            @click="setActiveStep(3)"
          >
            3. 실제 의견 보기
          </button>
        </nav>

        <section v-if="activeStep === 1" class="step-panel">
          <p class="section-kicker">정책 입력</p>
          <div class="policy-row">
            <label>
              <span>시뮬레이션</span>
              <select v-model="selectedSimulationId" class="policy-select" :disabled="scenarioLoading">
                <option value="">시뮬레이션 선택</option>
                <option
                  v-for="item in simulations"
                  :key="item.simulation_id"
                  :value="item.simulation_id"
                >
                  {{ item.simulation_id }}
                </option>
              </select>
            </label>

            <label>
              <span>타깃 정당</span>
              <select v-model="selectedParty" class="policy-select" :disabled="scenarioLoading">
                <option value="">정당 선택</option>
                <option
                  v-for="party in scenarioPartyOptions"
                  :key="party"
                  :value="party"
                >
                  {{ party }}
                </option>
              </select>
            </label>
          </div>

          <label class="policy-textarea-wrap">
            <span>정책안 텍스트</span>
            <textarea
              v-model="campaignText"
              rows="6"
              placeholder="정책안을 입력하면 해당 정당 지지도 변화 시뮬레이션에 반영됩니다."
            ></textarea>
          </label>

          <div class="step-actions">
            <button
              class="step-primary-btn"
              :disabled="scenarioLoading || !selectedSimulationId || !selectedParty"
              @click="saveScenario"
            >
              {{ scenarioLoading ? '저장 중...' : '시나리오 저장하고 다음 단계로' }}
            </button>
          </div>
        </section>

        <section v-else-if="activeStep === 2" class="step-panel">
          <div class="timeline-head">
            <div>
              <p class="section-kicker">실시간 지지도 변화</p>
              <strong>{{ selectedParty }} 기준</strong>
            </div>
            <div class="step-actions">
              <button
                class="step-primary-btn"
                :disabled="scenarioLoading || !selectedSimulationId || !selectedParty"
                @click="startSimulationRun"
              >
                {{
                  isSimulationRunning ? '실행 중...' : '지금 실행'
                }}
              </button>
              <button
                class="step-secondary-btn"
                @click="loadDemoData"
              >
                데모로 채우기
              </button>
              <button
                v-if="latestRound > 0"
                class="step-secondary-btn"
                @click="setActiveStep(3)"
              >
                지금 바로 의견 보기로 이동
              </button>
            </div>
          </div>

          <div class="timeline-chart-wrap">
            <svg ref="supportChartSvg" class="support-chart"></svg>
          </div>

          <p class="timeline-metrics">
            최근 라운드 {{ latestRound }} / 추정 지지도 {{ latestSupport.toFixed(1) }}%
          </p>
          <p class="policy-status">
            <span>{{ simulationStatusText }}</span>
            <strong>{{ scenarioMessage }}</strong>
          </p>
        </section>

        <section v-else class="step-panel">
          <div class="timeline-head">
            <div>
              <p class="section-kicker">실시간 여론 반응</p>
              <strong>누적 의견 피드</strong>
            </div>
            <button class="step-secondary-btn" @click="refreshOpinionFeed">
              새로고침
            </button>
          </div>

          <div v-if="opinionThreads.length > 0" class="opinion-list">
            <article
              v-for="thread in opinionThreads"
              :key="thread.round"
              class="opinion-thread"
            >
              <p class="opinion-thread-title">라운드 {{ thread.round }} 토론</p>
              <div
                v-for="item in thread.items"
                :key="item.key"
                class="opinion-card"
              >
                <div class="opinion-headline">
                  <span class="opinion-platform">{{ actionPlatformBadge(item.platform) }}</span>
                  <strong class="opinion-actor">{{ item.agent_name || `Agent ${item.agent_id || '미지정'}` }}</strong>
                  <span class="opinion-action">{{ actionDisplayName(item.action_type) }}</span>
                  <span class="opinion-stance" :class="opinionStanceClass(item)">{{ opinionStanceLabel(item) }}</span>
                </div>
                <p class="opinion-detail">{{ actionDisplayText(item) }}</p>
                <ul v-if="actionReasons(item).length" class="opinion-reasons">
                  <li v-for="reason in actionReasons(item)" :key="reason">{{ reason }}</li>
                </ul>
                <p v-else class="opinion-empty-reason">근거 문구가 없어 가상의 의견으로 처리했습니다.</p>
                <div class="opinion-meta">
                  <span>{{ item.timeLabel }}</span>
                  <span>{{ item.platform }}</span>
                  <span v-if="item.district">{{ item.district }}</span>
                  <span v-if="item?.persona_profile?.traits?.length">
                    {{ item.persona_profile.traits.join(', ') }}
                  </span>
                </div>
              </div>
            </article>
          </div>
          <p v-else class="support-empty">실행이 진행되면 이곳에 의견이 실시간으로 표시됩니다.</p>
        </section>

        <div v-if="selectedDistrict" class="district-snippet">
          <p class="district-snippet-head">
            현재 구 시뮬레이션 성향
            <strong>{{ selectedParty }} {{ getLivePartyShare(selectedDistrict).toFixed(1) }}%</strong>
          </p>
          <ul class="district-snippet-list">
            <li>선거인수: {{ toPopulation(selectedDistrict.profile.electorate) }}</li>
            <li>유효 투표수: {{ toPopulation(selectedDistrict.profile.validVotes) }}</li>
            <li>구당 지지도 기준: {{ selectedParty }}</li>
            <li>투표율: {{ selectedDistrict.profile.turnoutPercent }}%</li>
            <li>
              등록인구: {{ formatPopulation(selectedDistrict.profile.populationProfile.population) }}
              (남 {{ selectedDistrict.profile.populationProfile.maleRate }}% / 여 {{ selectedDistrict.profile.populationProfile.femaleRate }}%)
            </li>
          </ul>
        </div>

        <p v-else class="support-empty">지도에서 구를 클릭해서 구 정보를 확인하세요.</p>
      </aside>
    </section>
  </section>
</template>

<script setup>
import * as d3 from 'd3'
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import {
  getPrepareStatus,
  getRunStatus,
  getRunStatusDetail,
  getSimulation,
  getSimulationTimeline,
  listSimulations,
  prepareSimulation,
  startSimulation,
  updateSimulationScenario
} from '../api/simulation'

const mapSvg = ref(null)
const mapWrap = ref(null)
const loading = ref(true)
const error = ref('')
const districtFeatures = ref([])
const DEMO_SAMPLE_DATA_BASE_TIME = new Date().toISOString()
const activeParty = ref('all')
const supportChartSvg = ref(null)
const selectedCode = ref('')
const electionMeta = ref(null)
const populationMeta = ref(null)
const activeStep = ref(1)
const scenarioSaved = ref(false)
const isDemoMode = ref(false)
const opinionFeed = ref([])
const districtLiveSupport = ref({})
const simulationRounds = ref(12)
const simulationRoundMs = ref(1250)
const simulationPersonaPool = ref([])
let demoTimer = null

// 시뮬레이션/정책 패널
const simulations = ref([])
const selectedSimulationId = ref('')
const selectedParty = ref('더불어민주당')
const campaignText = ref('')
const scenarioMessage = ref('')
const scenarioLoading = ref(false)
const supportTimeline = ref([])
const runStatus = ref(null)

let runStatusTimer = null

const SIMULATION_PARTY_CONTEXTS = [
  '더불어민주당',
  '국민의힘',
  '개혁신당',
  '새로운미래',
  '녹색정의당',
  '무소속',
  '기타'
]

const PARTY_DEMO_TEMPLATES = [
  {
    id: 'single_parent',
    name: '아이 엄마',
    traits: ['양육 부담', '육아 지원 필요'],
    ageGroups: ['20-29', '30-39'],
    gender: ['여성'],
    stanceProfile: {
      policyBonus: { '주거': 0.18, '복지': 0.16, '교육': 0.12, '세금': -0.02 }
    }
  },
  {
    id: 'commuter',
    name: '장거리 통근자',
    traits: ['출퇴근 피로', '교통 인프라 개선 선호'],
    ageGroups: ['30-49', '40-59'],
    gender: ['남성', '여성'],
    stanceProfile: {
      policyBonus: { '교통': 0.2, '주거': 0.02, '환경': 0.08, '안전': 0.05 }
    }
  },
  {
    id: 'youth_worker',
    name: '청년 노동자',
    traits: ['채용 안정', '생계 비용 민감'],
    ageGroups: ['20-39'],
    gender: ['남성', '여성'],
    stanceProfile: {
      policyBonus: { '일자리': 0.22, '주거': 0.15, '교육': 0.05, '복지': 0.09 }
    }
  },
  {
    id: 'senior_resident',
    name: '장년 거주자',
    traits: ['복지 안정', '의료 접근성'],
    ageGroups: ['50+'],
    gender: ['남성', '여성'],
    stanceProfile: {
      policyBonus: { '건강': 0.18, '안전': 0.12, '교통': 0.08, '복지': 0.1 }
    }
  },
  {
    id: 'entrepreneur',
    name: '소상공인',
    traits: ['규제 완화', '세제 민감도'],
    ageGroups: ['20-59'],
    gender: ['남성', '여성'],
    stanceProfile: {
      policyBonus: { '세금': 0.16, '일자리': 0.09, '주거': -0.08, '교통': 0.02 }
    }
  }
]

const partyColorMap = {
  '더불어민주당': '#2563EB',
  '국민의힘': '#E11D48',
  '개혁신당': '#0EA5E9',
  '새로운미래': '#7C3AED',
  '녹색정의당': '#059669',
  '무소속': '#6B7280',
  '기타': '#94A3B8'
}

  const partyListFallback = ['더불어민주당', '국민의힘', '개혁신당', '새로운미래', '녹색정의당', '무소속', '기타']

const districtProfiles = ref({})
const legendItems = ref([
  { id: 'all', name: '전체', color: '#0f172a' },
  ...partyListFallback.map((party) => ({ id: party, name: party, color: partyColorMap[party] || '#94A3B8' }))
])

const normalizePopulationProfile = (districtName = '구', payload = {}) => {
  const safePayload = payload || {}

  return ({
  name: districtName,
  population: Number(safePayload.population) || 0,
  male: Number(safePayload.male) || 0,
  female: Number(safePayload.female) || 0,
  maleRate: Number(safePayload.maleRate) || 0,
  femaleRate: Number(safePayload.femaleRate) || 0,
  ageGroups: Array.isArray(safePayload.ageGroups)
    ? safePayload.ageGroups.map((group) => ({
      label: group.label || '미지정',
      total: Number(group.total) || 0,
      male: Number(group.male) || 0,
      female: Number(group.female) || 0,
      ratio: Number(group.ratio) || 0
    }))
    : []
  })
}

const makeFallbackProfile = (districtName = '구', populationProfile = {}) => ({
  name: districtName,
  electorate: 0,
  validVotes: 0,
  turnoutVotes: 0,
  turnoutPercent: 0,
  dominantParty: '기타',
  support: [
    { party: '더불어민주당', percent: 0, votes: 0 },
    { party: '국민의힘', percent: 0, votes: 0 },
    { party: '개혁신당', percent: 0, votes: 0 },
    { party: '새로운미래', percent: 0, votes: 0 },
    { party: '녹색정의당', percent: 0, votes: 0 },
    { party: '무소속', percent: 0, votes: 0 },
    { party: '기타', percent: 100, votes: 0 }
  ],
  note: '해당 구의 선거 집계 데이터가 없습니다.',
  populationProfile: normalizePopulationProfile(districtName, populationProfile),
  populationSource: '뉴스/보도 자료 기반 임시치, 추후 API 연동 예정'
})

const normalizeProfile = (districtName, profile = {}, populationProfile = null) => {
  const support = Array.isArray(profile.support) ? profile.support : []
  const sortedSupport = support
    .filter((item) => Number(item.percent) > 0)
    .map((item) => ({
      party: item.party || '기타',
      percent: Number(item.percent) || 0,
      votes: Number(item.votes) || 0
    }))
    .sort((a, b) => b.percent - a.percent)

  const fallback = makeFallbackProfile(districtName)
  const exists = new Set(sortedSupport.map((item) => item.party))
  const merged = [...sortedSupport]
  fallback.support.forEach((item) => {
    if (!exists.has(item.party)) {
      merged.push(item)
    }
  })

  const dominant = sortedSupport[0]?.party || fallback.dominantParty

  return {
    ...fallback,
    populationProfile: normalizePopulationProfile(districtName, populationProfile),
    name: districtName,
    electorate: Number(profile.electorate) || 0,
    validVotes: Number(profile.validVotes) || 0,
    turnoutVotes: Number(profile.turnoutVotes) || 0,
    turnoutPercent: Number(profile.turnoutPercent) || 0,
    dominantParty: profile.dominantParty || dominant,
    support: merged,
    note: profile.note || fallback.note,
    populationSource: profile.populationSource || fallback.populationSource
  }
}

const defaultProfile = {
  ...makeFallbackProfile('기본값'),
  note: '선거 집계 데이터가 준비되지 않았습니다.'
}

const activePartyLabel = computed(() => {
  if (activeParty.value === 'all') return '전체'
  return legendItems.value.find((item) => item.id === activeParty.value)?.name || '전체'
})

const dataSourceLabel = computed(() => {
  const electionSource = electionMeta.value?.source || '미확인 선거 데이터'
  const popSource = populationMeta.value?.source || '미확인 인구 데이터'
  return `선거=${electionSource} / 인구=${popSource}`
})

const selectedDistrict = computed(() => {
  return districtFeatures.value.find((d) => d.properties.code === selectedCode.value)
    || districtFeatures.value[0]
})

const partyColor = (party) => partyColorMap[party] || '#94A3B8'

const toPopulation = (value) => `${Number(value || 0).toLocaleString('ko-KR')}명`
const formatPopulation = (value) => `${Number(value || 0).toLocaleString('ko-KR')}명`

const setPartyFilter = (partyId) => {
  activeParty.value = partyId
  drawMap()
}

const clamp = (value, min, max) => Math.max(min, Math.min(max, value))

const currentPartyForMap = computed(() => {
  if (activeParty.value !== 'all') return activeParty.value
  if (selectedParty.value) return selectedParty.value
  return '더불어민주당'
})

const getDistrictSupportByParty = (feature, party = null) => {
  const targetParty = party || selectedParty.value
  const baseProfile = feature?.profile || {}
  const support = Array.isArray(baseProfile.support)
    ? baseProfile.support.find((item) => item.party === targetParty)?.percent
    : 0
  return Number(support || 0)
}

const districtPartyBaselineShare = (feature) => {
  const profile = feature?.profile || {}
  const base = profile?.support?.find((item) => item.party === selectedParty.value)
  return Number(base?.percent || 0)
}

const getLivePartyShare = (feature) => {
  const code = feature?.properties?.code
  if (!code) return districtPartyBaselineShare(feature)
  const live = districtLiveSupport.value[code]
  if (typeof live === 'number' && Number.isFinite(live)) {
    return clamp(live, 0, 100)
  }
  return districtPartyBaselineShare(feature)
}

const pickRandom = (arr) => arr[Math.floor(Math.random() * arr.length)]
const inferPopulationWeight = (district) => {
  const profile = district?.profile || {}
  const electorate = Number(profile.electorate || 0)
  return electorate > 0 ? electorate : Number(profile.populationProfile?.population || 10000)
}

const selectedSimulation = computed(() => {
  return simulations.value.find((item) => item.simulation_id === selectedSimulationId.value) || null
})

const isSimulationRunning = computed(() => {
  return demoTimer || ['running', 'starting'].includes(runStatus.value?.runner_status)
})

const setActiveStep = (step) => {
  activeStep.value = step
  if (
    step === 2 &&
    !supportTimeline.value.length &&
    !isDemoMode.value &&
    !isSimulationRunning.value
  ) {
    loadDemoData()
  }
  if (step === 2 || step === 3) {
    activeParty.value = selectedParty.value || 'all'
  }
}

const campaignSentimentSignal = (text = '') => {
  const normalized = String(text || '').toLowerCase()
  const positive = ['복지', '주거', '교육', '교통', '일자리', '안전', '환경', '안정', '청년']
  const negative = ['감세', '세금', '비용', '증가', '실행', '위험', '불안']
  let score = 0

  positive.forEach((word) => {
    if (normalized.includes(word)) score += 0.12
  })
  negative.forEach((word) => {
    if (normalized.includes(word)) score -= 0.06
  })

  return clamp(score, -0.35, 0.35)
}

const buildPersonaText = (persona, policy = '') => {
  const policySignal = campaignSentimentSignal(policy)
  return `${persona.ageBand} ${persona.gender}, ${persona.homeDistrict}의 ${persona.personaName} | ${persona.traits.join(' · ')} | 기초 지지도:${persona.influenceBias.toFixed(2)} / 정책 반영:${policySignal.toFixed(2)}`
}

const buildPersonaProfiles = () => {
  const profiles = []

  districtFeatures.value.forEach((district) => {
    const baseShare = getDistrictSupportByParty(district, selectedParty.value)
    const districtName = district.profile?.name || district.properties?.name || '서울'
    const districtCode = district.properties?.code
    const count = Math.max(10, Math.min(24, Math.round((district.populationProfile?.population || 12000) / 5000)))

    for (let i = 0; i < count; i++) {
      const tpl = pickRandom(PARTY_DEMO_TEMPLATES)
      const base = clamp((baseShare - 50) / 100, -0.55, 0.55)
      const policyBias = campaignSentimentSignal(campaignText.value) * 0.5
      const traitScore = (Math.random() - 0.5) * 0.3
      profiles.push({
        id: `${districtCode}-${tpl.id}-${i}`,
        code: districtCode,
        homeDistrict: districtName,
        personaName: tpl.name,
        ageBand: pickRandom(tpl.ageGroups),
        gender: pickRandom(tpl.gender),
        traits: tpl.traits,
        template: tpl,
        influenceBias: clamp(base + traitScore + policyBias, -1.1, 1.1)
      })
    }
  })

  simulationPersonaPool.value = profiles
  return profiles
}

const seedDistrictSupportState = () => {
  const seed = {}
  districtFeatures.value.forEach((district) => {
    const code = district.properties?.code
    if (code) {
      seed[code] = clamp(getDistrictSupportByParty(district, selectedParty.value), 0, 100)
    }
  })
  districtLiveSupport.value = seed
}

const aggregateCitySupport = () => {
  let weighted = 0
  let sumWeight = 0

  districtFeatures.value.forEach((district) => {
    const code = district.properties?.code
    if (!code) return
    const share = getLivePartyShare(district)
    const weight = inferPopulationWeight(district)
    weighted += share * weight
    sumWeight += weight
  })

  return sumWeight > 0 ? clamp(weighted / sumWeight, 0, 100) : 50
}

const simulateOpinionRound = (round) => {
  if (!simulationPersonaPool.value.length) {
    return { actors: [], districtDelta: {} }
  }

  const count = Math.max(4, Math.min(9, Math.round(simulationPersonaPool.value.length / 8)))
  const now = new Date().toISOString()
  const districtDelta = {}
  const actors = []
  const templates = [
    '정책 효익이 지역 통근자에게 체감되면 지지가 안정적으로 붙을 가능성이 높아요.',
    '구체 일정표와 우선순위가 보이면 신뢰가 올라갑니다.',
    '너무 큰 폭의 약속은 오히려 반발을 만들 수 있어요.',
    '가족·돌봄 비용 부담을 줄이면 공감도가 큽니다.',
    '현장 예산을 먼저 제시해야 대중이 움직입니다.',
    '전면 부정보다 개선형 보완안이 훨씬 설득력이 큽니다.'
  ]

  for (let i = 0; i < count; i++) {
    const actor = pickRandom(simulationPersonaPool.value)
    if (!actor || !actor.code) continue
    const tplBonus = Object.values(actor.template?.stanceProfile?.policyBonus || {}).reduce((sum, value) => sum + Number(value || 0), 0)
    const actionScore = clamp((actor.influenceBias * 0.8) + (tplBonus * 0.5) + (campaignSentimentSignal(campaignText.value) * 1.3) + (Math.random() - 0.5) * 0.9, -2.2, 2.2)
    const delta = actionScore * 0.22
    const prev = getLivePartyShare({ properties: { code: actor.code }, profile: districtFeatures.value.find((district) => district.properties?.code === actor.code)?.profile })
    const next = clamp(prev + delta, 3, 96)
    districtDelta[actor.code] = next

    const actionType = actionScore >= 0.55 ? 'endorsement' : actionScore <= -0.4 ? 'attack' : 'debate_response'
    actors.push({
      party: selectedParty.value,
      platform: Math.random() > 0.5 ? 'reddit' : 'twitter',
      action_type: actionType,
      agent_id: actor.id,
      agent_name: `${actor.homeDistrict} ${actor.personaName}`,
      district: actor.homeDistrict,
      round_num: round,
      timestamp: now,
      action_args: {
        content: `${buildPersonaText(actor, campaignText.value)} ${pickRandom(templates)}`,
        reasons: [
          `성향 점수 ${(actor.influenceBias).toFixed(2)}`,
          `정책 반응점수 ${(campaignSentimentSignal(campaignText.value)).toFixed(2)}`
        ],
        evidence: [
          `구 ${actor.homeDistrict} 토론 피드 반응`
        ],
        district_focus: actor.homeDistrict
      }
    })
  }

  const merged = { ...districtLiveSupport.value }
  Object.entries(districtDelta).forEach(([code, next]) => {
    merged[code] = next
  })
  districtLiveSupport.value = merged

  return {
    actors,
    districtDelta
  }
}

const stopDemoEngine = () => {
  if (demoTimer) {
    clearInterval(demoTimer)
    demoTimer = null
  }
}

const startDemoEngine = () => {
  if (!districtFeatures.value.length) return
  isDemoMode.value = true
  buildPersonaProfiles()
  seedDistrictSupportState()

  const maxRound = Number(simulationRounds.value || 12)
  const start = Number(aggregateCitySupport().toFixed(2))
  supportTimeline.value = [{ round_num: 0, support_snapshot: start }]

  opinionFeed.value = []
  runStatus.value = {
    runner_status: 'running',
    current_round: 0,
    total_rounds: maxRound
  }
  scenarioMessage.value = '데모 디베이트 엔진이 시작됩니다. 지지도 및 의견을 실시간으로 생성합니다.'
  let round = 1
  drawSupportChart()
  drawMap()
  stopDemoEngine()

  demoTimer = setInterval(() => {
    const { actors } = simulateOpinionRound(round)
    const current = aggregateCitySupport()
    const prev = supportTimeline.value[supportTimeline.value.length - 1]?.support_snapshot ?? current
    const drift = clamp(prev + (Math.random() - 0.5) * 0.9 + campaignSentimentSignal(campaignText.value), 0, 100)
    supportTimeline.value = [...supportTimeline.value, { round_num: round, support_snapshot: Number(drift.toFixed(2)) }]
    opinionFeed.value = normalizeOpinionItems([...actors, ...opinionFeed.value]).slice(0, 120)

    runStatus.value = {
      ...(runStatus.value || {}),
      runner_status: (round >= maxRound ? 'completed' : 'running'),
      current_round: round
    }

    drawSupportChart()
    drawMap()

  if (round >= maxRound) {
      stopDemoEngine()
      scenarioMessage.value = '데모 시뮬레이션이 완료되었습니다.'
    }
    round += 1
  }, Number(simulationRoundMs.value))
}

const actionDisplayName = (actionType = '') => {
  const actionTypeLabelMap = {
    policy_clarification: '정책 설명',
    district_targeted_message: '구별 메시지',
    attack: '공격 대응',
    apology: '사과/입장 정정',
    endorsement: '지지 표명',
    pledge_release: '공약 발표',
    debate_response: '토론 반응',
    scandal_response: '스캔들 대응',
    CREATE_POST: '게시글 생성',
    COMMENT_ANSWER: '댓글 응답',
    policy_update: '정책 업데이트',
    neutralization: '반응 정리'
  }

  return actionTypeLabelMap[actionType] || actionType || '의견 발언'
}

const actionDisplayText = (action = {}) => {
  const args = action.action_args || {}
  const result = action.result || {}
  if (typeof args.content === 'string' && args.content.trim()) return args.content.trim()
  if (typeof args.text === 'string' && args.text.trim()) return args.text.trim()
  if (typeof args.message === 'string' && args.message.trim()) return args.message.trim()
  if (typeof result.content === 'string' && result.content.trim()) return result.content.trim()
  if (typeof result.message === 'string' && result.message.trim()) return result.message.trim()

  return '실시간 의견이 기록되었습니다.'
}

const actionReasons = (action = {}) => {
  const args = action.action_args || {}
  const result = action.result || {}
  const reasons = []

  if (Array.isArray(args?.reasons)) {
    reasons.push(...args.reasons.filter(Boolean))
  }

  if (typeof args?.reason === 'string' && args.reason.trim()) {
    reasons.push(args.reason.trim())
  }
  if (typeof args?.reasoning === 'string' && args.reasoning.trim()) {
    reasons.push(args.reasoning.trim())
  }
  if (typeof result?.reason === 'string' && result.reason.trim()) {
    reasons.push(result.reason.trim())
  }
  if (typeof result?.reasoning === 'string' && result.reasoning.trim()) {
    reasons.push(result.reasoning.trim())
  }

  if (Array.isArray(args?.evidence)) {
    args.evidence.forEach((item) => {
      if (item) reasons.push(`근거: ${String(item)}`)
    })
  }
  if (Array.isArray(args?.counter_arguments)) {
    args.counter_arguments.forEach((item) => {
      if (item) reasons.push(`반론: ${String(item)}`)
    })
  }

  return reasons.map((reason) => String(reason).trim()).filter(Boolean)
}

const opinionStanceLabel = (action = {}) => {
  const content = (
    action?.action_args?.content ||
    action?.action_args?.text ||
    action?.action_args?.message ||
    action?.result?.content ||
    action?.result?.message ||
    action?.action_type ||
    ''
  ).toString().toLowerCase()

  const positiveKeywords = ['찬성', '환영', '호응', '긍정', '좋', '동의', '지지', '지원', '유리', '개선', '완화']
  const negativeKeywords = ['우려', '반대', '비판', '불신', '문제', '불만', '부담', '위험', '반발', '비난', '우려감']

  if (negativeKeywords.some((key) => content.includes(key))) return '비판'
  if (positiveKeywords.some((key) => content.includes(key))) return '지지'
  return '중립'
}

const opinionStanceClass = (action = {}) => {
  const stance = opinionStanceLabel(action)
  if (stance === '지지') return 'stance-boost'
  if (stance === '비판') return 'stance-risk'
  return 'stance-neutral'
}

const opinionThreads = computed(() => {
  const grouped = new Map()
  opinionFeed.value.forEach((item) => {
    const roundKey = Number(item.round_num || 0)
    if (!grouped.has(roundKey)) {
      grouped.set(roundKey, [])
    }
    grouped.get(roundKey).push(item)
  })

  return Array.from(grouped.entries())
    .map(([round, items]) => ({
      round,
      items: items
        .slice()
        .sort((a, b) => {
          const t1 = new Date(a.timestamp || 0).getTime()
          const t2 = new Date(b.timestamp || 0).getTime()
          if (Number.isNaN(t1) && Number.isNaN(t2)) return 0
          if (Number.isNaN(t1)) return 1
          if (Number.isNaN(t2)) return -1
          return t1 - t2
        })
    }))
    .sort((a, b) => b.round - a.round)
})

const actionPlatformBadge = (platform = '') => {
  if (platform === 'reddit') return 'Reddit'
  if (platform === 'twitter') return 'X'
  return platform || 'OPINION'
}

const actionTimeLabel = (raw) => {
  if (!raw) return ''
  const date = new Date(raw)
  if (Number.isNaN(date.getTime())) return ''

  return `${date.toLocaleDateString()} ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`
}

const scenarioPartyOptions = computed(() => {
  const optionSet = new Set()
  partyListFallback.forEach((party) => optionSet.add(party))

  const simulationParty = selectedSimulation.value?.candidate_profiles || []
  simulationParty.forEach((item) => {
    if (typeof item === 'string') {
      optionSet.add(item)
    } else if (item?.party) {
      optionSet.add(item.party)
    } else if (item?.candidate_name) {
      optionSet.add(item.candidate_name)
    }
  })

  return Array.from(optionSet)
})

const simulationStatusText = computed(() => {
  if (runStatus.value?.runner_status) {
    const map = {
      running: '실시간 실행 중',
      starting: '시작 대기',
      completed: '완료',
      failed: '실패',
      stopped: '중단',
      idle: '대기 중'
    }
    return map[runStatus.value.runner_status] || runStatus.value.runner_status
  }

  return selectedSimulation.value?.status || '미실행'
})

const latestRound = computed(() => {
  const list = supportTimeline.value
  if (!list || list.length === 0) return 0
  return list[list.length - 1]?.round_num || 0
})

const latestSupport = computed(() => {
  const list = supportTimeline.value
  if (!list || list.length === 0) return 50
  return list[list.length - 1]?.support_snapshot ?? 50
})

const normalizeOpinionItems = (items = []) => {
  return (items || []).map((item, index) => ({
    ...item,
    key: `${item.timestamp || item.created_at || '0'}-${item.platform || 'platform'}-${item.agent_id || index}-${index}`,
    timeLabel: actionTimeLabel(item.timestamp || item.created_at)
  }))
}

const loadDemoData = () => {
  isDemoMode.value = true
  activeParty.value = selectedParty.value || '더불어민주당'
  simulationRounds.value = 8
  startDemoEngine()
  scenarioMessage.value = '데모 데이터로 지지도 추세와 의견 피드를 즉시 생성합니다.'
  drawSupportChart()
}

const stopRealtimePolling = () => {
  stopDemoEngine()

  if (runStatusTimer) {
    clearInterval(runStatusTimer)
    runStatusTimer = null
  }

}

const waitUntilPrepared = async (simulationId, taskId = null) => {
  let attempts = 0
  const maxAttempts = 240

  while (attempts < maxAttempts) {
    const check = await getPrepareStatus({
      simulation_id: simulationId,
      task_id: taskId
    })

    const data = check.data
    if (data?.status === 'ready' || data?.status === 'completed') {
      return
    }

    if (data?.status === 'error' || data?.status === 'failed') {
      throw new Error(data?.error || 'Prepare failed')
    }

    await new Promise((resolve) => setTimeout(resolve, 1200))
    attempts += 1
  }

  throw new Error('시뮬레이션 준비가 4분 초과되어 중단되었습니다.')
}

const pollSimulationStatus = async () => {
  if (!selectedSimulationId.value) return

  try {
    const statusResponse = await getRunStatus(selectedSimulationId.value)
    const detailResponse = await getRunStatusDetail(selectedSimulationId.value)
    runStatus.value = statusResponse.data

    if (detailResponse?.data) {
      const detailed = detailResponse.data
      runStatus.value = {
        ...runStatus.value,
        ...detailed
      }

      if (Array.isArray(detailed.recent_actions)) {
        opinionFeed.value = normalizeOpinionItems(detailed.recent_actions)
      } else if (Array.isArray(detailed.all_actions)) {
        opinionFeed.value = normalizeOpinionItems(detailed.all_actions)
      }
    }

    const timelineResponse = await getSimulationTimeline(
      selectedSimulationId.value,
      0,
      null,
      selectedParty.value
    )
    supportTimeline.value = timelineResponse.data?.timeline || []

    drawSupportChart()

    if (
      runStatus.value?.runner_status &&
      !['running', 'starting'].includes(runStatus.value.runner_status)
    ) {
      stopRealtimePolling()
    }
  } catch (e) {
    console.error('pollSimulationStatus failed', e)
  }
}

const startRealtimePolling = () => {
  isDemoMode.value = false
  stopRealtimePolling()
  runStatusTimer = setInterval(() => {
    pollSimulationStatus()
  }, 1500)

  pollSimulationStatus()
}

const loadSimulationDetails = async (simulationId) => {
  const detailResponse = await getSimulation(simulationId)
  const data = detailResponse.data || null

  campaignText.value = (data?.campaign_action_brief || '').replace(/^\[선정 정당:[^\]]+\]\s*/g, '').trim()

  const candidateProfiles = Array.isArray(data?.candidate_profiles) ? data.candidate_profiles : []
  const firstProfileParty = candidateProfiles.find((item) => {
    if (typeof item === 'string') return item
    return item?.party || item?.candidate_name
  })

  const normalizedFirst =
    typeof firstProfileParty === 'string'
      ? firstProfileParty
      : firstProfileParty?.party || firstProfileParty?.candidate_name

  if (normalizedFirst && !selectedParty.value) {
    selectedParty.value = normalizedFirst
  }

  if (!selectedParty.value && scenarioPartyOptions.value.length > 0) {
    selectedParty.value = scenarioPartyOptions.value[0]
  }

  if (!selectedParty.value) {
    selectedParty.value = SIMULATION_PARTY_CONTEXTS[0]
  }
  activeParty.value = selectedParty.value

  scenarioSaved.value = false
  isDemoMode.value = false

  runStatus.value = {
    runner_status: data?.status || 'idle'
  }

  opinionFeed.value = []
}

const loadSimulations = async () => {
  const response = await listSimulations()
  simulations.value = response.data || []

  if (!selectedSimulationId.value && simulations.value.length > 0) {
    selectedSimulationId.value = simulations.value[0].simulation_id
    await loadSimulationDetails(simulations.value[0].simulation_id)
  }
}

const saveScenario = async () => {
  if (!selectedSimulationId.value) {
    scenarioMessage.value = '시뮬레이션을 먼저 선택해 주세요.'
    return
  }

  if (!selectedParty.value) {
    scenarioMessage.value = '정당을 먼저 선택해 주세요.'
    return
  }

  scenarioLoading.value = true
  scenarioMessage.value = '시나리오를 반영하고 있습니다.'

  try {
    await updateSimulationScenario(selectedSimulationId.value, {
      selected_party: selectedParty.value,
      campaign_action_brief: campaignText.value
    })
    activeParty.value = selectedParty.value
    scenarioSaved.value = true
    scenarioMessage.value = '시나리오가 저장되었습니다. 다음 단계에서 실행해 주세요.'
    activeStep.value = 2
  } catch (e) {
    scenarioMessage.value = `실행 중 오류: ${e?.message || '알 수 없는 오류'}`
    stopRealtimePolling()
  } finally {
    scenarioLoading.value = false
  }
}

const startSimulationRun = async () => {
  if (!selectedSimulationId.value) {
    scenarioMessage.value = '시뮬레이션을 먼저 선택해 주세요.'
    return
  }

  if (!selectedParty.value) {
    scenarioMessage.value = '정당을 먼저 선택해 주세요.'
    return
  }

  if (!scenarioSaved.value) {
    scenarioMessage.value = '정책과 정당 설정을 먼저 저장해 주세요.'
    activeStep.value = 1
    return
  }

  scenarioLoading.value = true
  scenarioMessage.value = '시뮬레이션을 준비하고 실행을 시작합니다.'

  try {
    const prepareResult = await prepareSimulation({
      simulation_id: selectedSimulationId.value
    })

    const prepareData = prepareResult.data || {}
    if (!prepareData.already_prepared && prepareData.task_id) {
      await waitUntilPrepared(selectedSimulationId.value, prepareData.task_id)
    }

    await startSimulation({
      simulation_id: selectedSimulationId.value,
      platform: 'parallel',
      force: true
    })

    scenarioMessage.value = '실행 중입니다. 추이와 의견을 함께 확인해 주세요.'
    startRealtimePolling()
    activeStep.value = 2
  } catch (e) {
    scenarioMessage.value = `실행 중 오류: ${e?.message || '알 수 없는 오류'}`
    startDemoEngine()
  } finally {
    scenarioLoading.value = false
  }
}

const refreshOpinionFeed = async () => {
  if (isDemoMode.value) {
    return
  }
  if (!selectedSimulationId.value) return

  try {
    const response = await getRunStatusDetail(selectedSimulationId.value)
    const detail = response?.data || {}
    const source = detail.recent_actions || detail.all_actions || []
    opinionFeed.value = normalizeOpinionItems(source)
  } catch (e) {
    console.error('refreshOpinionFeed failed', e)
  }
}

const drawSupportChart = async () => {
  if (!supportChartSvg.value) return

  const svg = d3.select(supportChartSvg.value)
  const hostRect = supportChartSvg.value.parentElement?.getBoundingClientRect() || { width: 520, height: 220 }
  const width = Math.max(320, Math.round(hostRect.width || 520))
  const height = Math.max(180, Math.round(hostRect.height || 220))
  const margin = { top: 14, right: 16, bottom: 24, left: 42 }

  supportChartSvg.value.setAttribute('viewBox', `0 0 ${width} ${height}`)
  svg.selectAll('*').remove()

  if (!supportTimeline.value.length) {
    svg.append('text')
      .attr('x', margin.left)
      .attr('y', height / 2)
      .attr('fill', '#94a3b8')
      .attr('font-size', 12)
      .text('실행을 시작하면 라운드별 지지도 추세가 표시됩니다.')

    return
  }

  const chartData = supportTimeline.value
    .map((item) => ({
      round_num: Number(item.round_num || 0),
      support_snapshot: Number(item.support_snapshot || 50)
    }))
    .sort((a, b) => a.round_num - b.round_num)

  const x = d3.scaleLinear()
    .domain(d3.extent(chartData, (item) => item.round_num))
    .range([margin.left, width - margin.right])

  const y = d3.scaleLinear()
    .domain([0, 100])
    .range([height - margin.bottom, margin.top])

  const axisY = d3.axisLeft(y)
    .ticks(5)
    .tickSize(-(width - margin.left - margin.right))

  const axisX = d3.axisBottom(x)
    .ticks(Math.min(8, Math.max(2, chartData.length)))

  svg
    .append('g')
    .attr('transform', `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(5).tickSize(0))
    .selectAll('text')
    .attr('fill', '#94a3b8')

  svg
    .append('g')
    .attr('transform', `translate(0, ${height - margin.bottom})`)
    .call(axisX)
    .selectAll('text')
    .attr('fill', '#94a3b8')

  svg
    .append('g')
    .attr('transform', `translate(${margin.left},0)`)
    .call(axisY)
    .selectAll('text')
    .attr('fill', '#94a3b8')

  svg.selectAll('.tick line')
    .attr('stroke', 'rgba(148, 163, 184, 0.2)')

  const line = d3.line()
    .x((d) => x(d.round_num))
    .y((d) => y(d.support_snapshot))
    .curve(d3.curveMonotoneX)

  svg
    .append('path')
    .datum(chartData)
    .attr('fill', 'none')
    .attr('stroke', '#60a5fa')
    .attr('stroke-width', 2.6)
    .attr('d', line)

  svg
    .selectAll('circle')
    .data(chartData)
    .join('circle')
    .attr('cx', (d) => x(d.round_num))
    .attr('cy', (d) => y(d.support_snapshot))
    .attr('r', 3)
    .attr('fill', '#dbeafe')

  const lastItem = chartData[chartData.length - 1]
  svg
    .append('text')
    .attr('x', width - margin.right)
    .attr('y', y(lastItem.support_snapshot) - 6)
    .attr('text-anchor', 'end')
    .attr('fill', '#e2e8f0')
    .attr('font-size', '12px')
    .text(`${lastItem.support_snapshot.toFixed(1)}%`)
}

const drawMap = async () => {
  if (!mapSvg.value || districtFeatures.value.length === 0) return

  const svg = d3.select(mapSvg.value)
  const wrapRect = mapWrap.value?.getBoundingClientRect()
  const width = Math.max(320, Math.round(wrapRect?.width || 940))
  const height = Math.max(260, Math.round(width * 0.7))

  mapSvg.value.setAttribute('viewBox', `0 0 ${width} ${height}`)
  svg.selectAll('*').remove()

  const projection = d3.geoMercator()
    .fitSize([width - 80, height - 80], {
      type: 'FeatureCollection',
      features: districtFeatures.value
    })

  const path = d3.geoPath(projection)
  const zoom = 1.1
  const g = svg
    .append('g')
    .attr('transform', `translate(${(width - 80) * 0.06}, ${(height - 80) * 0.06}) scale(${zoom})`)

  const districts = g
    .selectAll('.district')
    .data(districtFeatures.value)
    .join('path')
    .attr('class', 'district')
    .attr('d', path)
    .attr('data-code', (d) => d.properties.code)
    .attr('fill', (d) => {
      const targetParty = currentPartyForMap.value
      const party = targetParty || d.profile?.dominantParty || '기타'
      const raw = d3.color(partyColor(party)) || d3.color('#94A3B8')
      const share = getLivePartyShare(d)
      const intensity = clamp(0.2 + (share / 100) * 0.75, 0.18, 0.95)
      const dimmed = activeParty.value !== 'all' && targetParty !== 'all' && targetParty && party !== activeParty.value
      raw.opacity = dimmed ? 0.2 : intensity
      return raw.toString()
    })
    .attr('stroke', '#ffffffd9')
    .attr('stroke-width', 1.2)
    .attr('cursor', 'pointer')
    .on('click', (_, feature) => {
      selectedCode.value = feature.properties.code
      drawMap()
    })
    .on('mouseenter', (event, feature) => {
      const shape = d3.select(event.currentTarget)
      shape.attr('stroke', '#111827')
      shape.attr('stroke-width', 2.2)
    })
    .on('mouseleave', () => {
      drawMap()
    })

  districts.each((feature, index, nodes) => {
    const isActive = feature.properties.code === selectedCode.value
    const compareParty = currentPartyForMap.value
    const isFiltered = activeParty.value === 'all' || compareParty === 'all' || feature.profile?.dominantParty === activeParty.value || getLivePartyShare(feature) > 0
    const node = d3.select(nodes[index])
    node.classed('is-selected', isActive)
    node.classed('is-filtered', isFiltered)
    node.attr('opacity', isFiltered ? 1 : 0.25)
  })

  const centroidGroup = g.append('g')
    .attr('class', 'district-label-group')
    .attr('pointer-events', 'none')

  centroidGroup
    .selectAll('text')
    .data(districtFeatures.value)
    .join('text')
    .attr('text-anchor', 'middle')
    .attr('dy', '.35em')
    .text((d) => `${Math.round(getLivePartyShare(d))}%`)
    .attr('font-size', '10px')
    .attr('font-family', 'JetBrains Mono, monospace')
    .attr('fill', '#0f172a')
    .attr('x', (d) => {
      const c = path.centroid(d)
      return c[0] || 0
    })
    .attr('y', (d) => {
      const c = path.centroid(d)
      return c[1] || 0
    })
    .attr('opacity', 0.65)
    .style('paint-order', 'stroke')
    .style('stroke', '#ffffff')
    .style('stroke-width', '2.2px')
    .style('display', () => (activeParty.value === 'all' ? 'none' : 'block'))

  await nextTick()
}

const loadMapData = async () => {
  loading.value = true
  error.value = ''
  try {
    const [mapResponse, profileResponse, populationResponse] = await Promise.all([
      fetch('/seoul/seoul-municipalities-geo.json'),
      fetch('/seoul/party-support-2024.json'),
      fetch('/seoul/district-population-2026-02-28.json')
    ])

    if (!mapResponse.ok) {
      throw new Error('서울 구 경계 데이터를 불러오지 못했습니다.')
    }
    if (!profileResponse.ok) {
      throw new Error('서울 구 선거 득표 데이터를 불러오지 못했습니다.')
    }

    const [geo, profilePayload] = await Promise.all([
      mapResponse.json(),
      profileResponse.json()
    ])

    let populationPayload = { districts: [] }
    if (populationResponse.ok) {
      populationPayload = await populationResponse.json()
    }

    const populationByName = {}
    ;(populationPayload?.districts || []).forEach((item) => {
      if (item?.name) {
        populationByName[item.name] = item
      }
    })

    const profileByName = {}
    ;(profilePayload?.districts || []).forEach((item) => {
      const normalized = normalizeProfile(item?.name, item, populationByName[item?.name])
      profileByName[normalized.name] = normalized
      districtProfiles.value[normalized.name] = normalized
    })

    electionMeta.value = profilePayload?.metadata || null
    populationMeta.value = populationPayload?.metadata || null

    const parties = (electionMeta.value?.parties || partyListFallback).filter((party) => typeof party === 'string' && party)
    legendItems.value = [
      { id: 'all', name: '전체', color: '#0f172a' },
      ...parties.map((party) => ({ id: party, name: party, color: partyColorMap[party] || '#94A3B8' }))
    ]

    districtFeatures.value = geo.features.map((feature) => {
      const name = feature.properties?.name
      const profile = profileByName[name] || normalizeProfile(name, defaultProfile, populationByName[name])
      return {
        ...feature,
        profile,
        properties: {
          ...feature.properties,
          population: profile.populationProfile.population
        }
      }
    })
    districtFeatures.value.sort((a, b) => a.properties.name.localeCompare(b.properties.name))
    selectedCode.value = districtFeatures.value[0]?.properties.code || ''
    loading.value = false
    await nextTick()
    drawMap()
  } catch (e) {
    error.value = e.message
    loading.value = false
  }
}

onMounted(() => {
  Promise.all([loadMapData(), loadSimulations()])
  activeParty.value = selectedParty.value
})

onUnmounted(() => {
  stopRealtimePolling()
})

watch(() => [activeParty.value, selectedCode.value], () => {
  if (!loading.value) {
    drawMap()
  }
})

watch(() => selectedSimulationId.value, async (value) => {
  if (!value) return
  isDemoMode.value = false
  stopRealtimePolling()
  await loadSimulationDetails(value)
  scenarioMessage.value = ''
  scenarioSaved.value = false
  activeStep.value = 1
})

watch(() => supportTimeline.value, () => {
  nextTick(() => {
    drawSupportChart()
  })
}, {
  deep: true
})

watch(() => selectedParty.value, () => {
  if (isDemoMode.value) {
    activeParty.value = selectedParty.value
    drawMap()
  }
  if (!supportTimeline.value.length) return
  if (!isDemoMode.value) {
    pollSimulationStatus()
  }
  scenarioSaved.value = false
})
</script>

<style scoped>
.seoul-page {
  min-height: 100vh;
  padding: 28px 24px 48px;
  background:
    linear-gradient(145deg, #111827 0%, #1e293b 30%, #334155 100%);
  color: #e2e8f0;
  font-family: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
}

.hero {
  max-width: 1200px;
  margin: 0 auto;
  padding: 14px 0 24px;
}

.hero-eyebrow {
  margin: 0;
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  color: #cbd5e1;
}

.hero h1 {
  margin: 12px 0 8px;
  color: #f8fafc;
  font-size: clamp(1.8rem, 3vw, 2.8rem);
  letter-spacing: -0.02em;
}

.hero-copy {
  margin: 0;
  max-width: 880px;
  color: #cbd5e1;
  line-height: 1.8;
}

.main-grid {
  max-width: 1280px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(340px, 0.9fr);
  gap: 28px;
}

.map-shell {
  padding: 16px;
  border: 1px solid rgba(226, 232, 240, 0.2);
  border-radius: 16px;
  position: relative;
  background:
    radial-gradient(circle at 12% 8%, rgba(59, 130, 246, 0.28), transparent 34%),
    linear-gradient(175deg, rgba(15, 23, 42, 0.9), rgba(15, 23, 42, 1));
  box-shadow: 0 28px 68px rgba(2, 6, 23, 0.35), inset 0 0 0 1px rgba(255, 255, 255, 0.04);
}

.map-frame {
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  background:
    linear-gradient(125deg, rgba(30, 41, 59, 0.94), rgba(15, 23, 42, 0.96));
  min-height: 640px;
  display: flex;
  align-items: stretch;
}

.map-wrap {
  position: relative;
  width: 100%;
  height: 100%;
}

.map-lights,
.map-shadow {
  position: absolute;
  width: 220px;
  height: 220px;
  border-radius: 50%;
  pointer-events: none;
  z-index: 2;
}

.map-lights {
  top: -20px;
  right: 10%;
  background: radial-gradient(circle, rgba(96, 165, 250, 0.26), transparent 70%);
  filter: blur(2px);
}

.map-shadow {
  bottom: 12px;
  left: 14%;
  background: radial-gradient(circle, rgba(15, 23, 42, 0.22), transparent 72%);
}

.seoul-map {
  width: 100%;
  height: 760px;
  min-height: 620px;
  transform: translateZ(0);
}

.step-tabs {
  margin-top: 10px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.step-tab {
  border: 1px solid rgba(148, 163, 184, 0.28);
  background: rgba(15, 23, 42, 0.82);
  color: #cbd5e1;
  border-radius: 10px;
  padding: 10px 12px;
  cursor: pointer;
  font-family: 'Space Grotesk', 'Noto Sans SC', sans-serif;
  font-size: 0.78rem;
  transition: 160ms ease;
}

.step-tab.is-active {
  border-color: rgba(96, 165, 250, 0.85);
  color: #f8fafc;
  box-shadow: inset 0 0 0 1px rgba(96, 165, 250, 0.45);
}

.step-panel {
  margin-top: 12px;
  background: rgba(2, 6, 23, 0.52);
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 14px;
  padding: 12px;
}

.section-kicker {
  margin: 0 0 8px;
  color: #94a3b8;
  font-size: 0.76rem;
  letter-spacing: 0.05em;
}

.step-actions {
  margin-top: 10px;
  display: grid;
  gap: 8px;
}

.step-primary-btn,
.step-secondary-btn {
  border: 0;
  border-radius: 10px;
  font-family: 'Space Grotesk', 'Noto Sans SC', sans-serif;
  font-weight: 700;
  cursor: pointer;
  height: 40px;
  padding: 0 14px;
}

.step-primary-btn {
  width: 100%;
  color: #0f172a;
  background: linear-gradient(130deg, #38bdf8, #818cf8);
}

.step-primary-btn:disabled {
  cursor: not-allowed;
  background: #334155;
  color: #94a3b8;
}

.step-secondary-btn {
  color: #e2e8f0;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(148, 163, 184, 0.25);
}

.step-secondary-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.opinion-list {
  margin: 10px 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.opinion-thread {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-bottom: 8px;
  border-bottom: 1px dashed rgba(148, 163, 184, 0.2);
}

.opinion-thread-title {
  margin: 0;
  color: #e2e8f0;
  font-weight: 600;
  font-size: 0.76rem;
  letter-spacing: 0.05em;
  color: #cbd5e1;
}

.opinion-card {
  background: rgba(15, 23, 42, 0.58);
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 10px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.opinion-headline {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
}

.opinion-actor {
  color: #f8fafc;
  font-weight: 600;
}

.opinion-action {
  color: #a5b4fc;
  font-size: 0.72rem;
}

.opinion-stance {
  font-size: 0.68rem;
  border-radius: 999px;
  padding: 2px 8px;
  font-weight: 600;
  letter-spacing: 0.03em;
}

.stance-boost {
  background: rgba(34, 197, 94, 0.16);
  color: #86efac;
}

.stance-risk {
  background: rgba(239, 68, 68, 0.16);
  color: #fda4af;
}

.stance-neutral {
  background: rgba(148, 163, 184, 0.16);
  color: #cbd5e1;
}

.opinion-platform {
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  border-radius: 999px;
  padding: 2px 8px;
  background: rgba(96, 165, 250, 0.16);
  color: #93c5fd;
  text-transform: uppercase;
}

.opinion-detail {
  margin: 8px 0 4px;
  color: #cbd5e1;
  line-height: 1.5;
  font-size: 0.82rem;
  white-space: pre-wrap;
}

.opinion-reasons {
  margin: 0;
  padding: 0 0 0 14px;
  list-style: disc;
  color: #94a3b8;
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 0.76rem;
}

.opinion-empty-reason {
  margin: 2px 0 0;
  font-size: 0.74rem;
  color: #94a3b8;
}

.opinion-meta {
  margin: 0;
  color: #94a3b8;
  font-size: 0.72rem;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.district-snippet {
  margin-top: 12px;
  border-radius: 12px;
  background: rgba(30, 41, 59, 0.64);
  border: 1px solid rgba(148, 163, 184, 0.2);
  padding: 10px 12px;
}

.district-snippet-head {
  margin: 0 0 8px;
  color: #cbd5e1;
  font-size: 0.84rem;
  display: flex;
  justify-content: space-between;
}

.district-snippet-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 5px;
  color: #e2e8f0;
  font-size: 0.79rem;
}

.district {
  transition: transform 220ms ease, opacity 180ms ease, stroke 160ms ease;
  transform-origin: center center;
  filter: drop-shadow(0 2px 4px rgba(2, 6, 23, 0.25));
}

.district.is-selected {
  stroke: #f8fafc;
  stroke-width: 2.2px;
  filter: drop-shadow(0 8px 14px rgba(2, 6, 23, 0.45));
}

.district.is-filtered {
  transition: opacity 200ms ease;
}

.district:hover {
  transform: scale(1.015);
}

.map-mask {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.7);
  color: #f8fafc;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 4;
}

.map-mask--error {
  background: rgba(127, 29, 29, 0.8);
}

.legend-row {
  position: relative;
  z-index: 6;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 8px;
  padding-top: 10px;
}

.legend-pill {
  border: 1px solid rgba(226, 232, 240, 0.22);
  background: rgba(15, 23, 42, 0.7);
  color: #e2e8f0;
  padding: 10px 12px;
  border-radius: 999px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  cursor: pointer;
  transition: 180ms;
  position: relative;
}

.legend-pill::before {
  content: '';
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: var(--party-color);
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
}

.legend-pill span {
  margin-left: 14px;
}

.legend-pill.active,
.legend-pill:hover {
  background: rgba(241, 245, 249, 0.12);
  border-color: rgba(241, 245, 249, 0.45);
}

.detail-pane {
  border: 1px solid rgba(226, 232, 240, 0.2);
  border-radius: 16px;
  padding: 20px;
  background: rgba(15, 23, 42, 0.84);
  backdrop-filter: blur(3px);
  box-shadow: 0 18px 30px rgba(2, 6, 23, 0.45);
}

.detail-head {
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
  padding-bottom: 14px;
  margin-bottom: 16px;
}

.policy-ops {
  background: rgba(2, 6, 23, 0.55);
  border: 1px solid rgba(148, 163, 184, 0.28);
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.policy-kicker {
  margin: 0;
  color: #94a3b8;
  font-size: 0.76rem;
  letter-spacing: 0.06em;
}

.policy-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.policy-row label,
.policy-textarea-wrap {
  display: block;
  color: #cbd5e1;
  font-size: 0.8rem;
  letter-spacing: 0.02em;
}

.policy-row span,
.policy-textarea-wrap span {
  display: block;
  margin-bottom: 6px;
}

.policy-select,
.policy-textarea-wrap textarea {
  width: 100%;
  border: 1px solid rgba(148, 163, 184, 0.4);
  border-radius: 10px;
  background: rgba(15, 23, 42, 0.9);
  color: #f8fafc;
  padding: 10px;
  font: inherit;
}

.policy-textarea-wrap textarea {
  resize: vertical;
  min-height: 112px;
}

.policy-apply-btn {
  border: 0;
  background: linear-gradient(130deg, #38bdf8, #818cf8);
  color: #0f172a;
  border-radius: 12px;
  font-family: 'Space Grotesk', 'Noto Sans SC', sans-serif;
  font-weight: 700;
  padding: 12px;
  cursor: pointer;
  transition: 180ms;
}

.policy-apply-btn:hover:not(:disabled) {
  filter: brightness(1.07);
}

.policy-apply-btn:disabled {
  background: #334155;
  cursor: not-allowed;
  color: #94a3b8;
}

.policy-status {
  margin: 0;
  color: #94a3b8;
  display: grid;
  gap: 2px;
  font-size: 0.8rem;
}

.policy-status strong {
  color: #e2e8f0;
}

.timeline-panel {
  margin-bottom: 16px;
  background: rgba(2, 6, 23, 0.42);
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 14px;
  padding: 12px;
}

.timeline-head {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  color: #e2e8f0;
}

.timeline-head p {
  margin: 0;
  font-size: 0.78rem;
  letter-spacing: 0.03em;
  color: #94a3b8;
}

.timeline-head strong {
  font-size: 0.78rem;
  color: #f8fafc;
}

.timeline-chart-wrap {
  background: rgba(15, 23, 42, 0.74);
  border: 1px solid rgba(148, 163, 184, 0.28);
  border-radius: 12px;
  min-height: 220px;
  display: flex;
}

.support-chart {
  width: 100%;
  min-height: 220px;
}

.timeline-metrics {
  margin: 8px 0 0;
  color: #94a3b8;
  font-size: 0.78rem;
}

.detail-kicker {
  margin: 0;
  color: #94a3b8;
  font-size: 0.72rem;
  letter-spacing: 0.06em;
}

.detail-head h2 {
  margin: 8px 0 0;
  color: #f8fafc;
  font-size: 1.6rem;
}

.support-board {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.support-lead {
  margin: 0;
  color: #cbd5e1;
  font-size: 0.95rem;
}

.support-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.support-stats article {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 12px;
}

.support-stats p {
  margin: 0;
  color: #94a3b8;
  font-size: 0.74rem;
  letter-spacing: 0.02em;
}

.support-stats strong {
  display: block;
  margin-top: 4px;
  color: #f8fafc;
}

.support-title {
  margin-top: 12px;
  margin-bottom: 10px;
  color: #e2e8f0;
  font-size: 0.92rem;
  font-weight: 500;
}

.support-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.support-list li {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 10px 12px;
}

.support-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.84rem;
}

.support-meta strong {
  font-size: 0.86rem;
}

.support-track {
  margin-top: 8px;
  width: 100%;
  height: 10px;
  background: #0f172a;
  border-radius: 6px;
  overflow: hidden;
}

.support-fill {
  display: block;
  height: 100%;
}

.resident-note {
  background: rgba(30, 41, 59, 0.6);
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.2);
  padding: 12px;
  color: #cbd5e1;
  line-height: 1.6;
  font-size: 0.88rem;
}

.population-title {
  margin-top: 6px;
  color: #e2e8f0;
  font-size: 0.92rem;
  font-weight: 500;
}

.population-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.population-grid article {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 10px;
}

.population-grid p {
  margin: 0;
  color: #94a3b8;
  font-size: 0.74rem;
}

.population-grid strong {
  display: block;
  margin-top: 4px;
  color: #f8fafc;
}

.age-breakdown-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 8px;
}

.age-breakdown-list li {
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: 10px;
  row-gap: 2px;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 10px 12px;
  align-items: center;
}

.age-breakdown-list span {
  color: #cbd5e1;
  font-size: 0.82rem;
}

.age-breakdown-list strong {
  color: #f8fafc;
  justify-self: end;
  font-size: 0.84rem;
}

.age-breakdown-list small {
  grid-column: 1 / -1;
  color: #94a3b8;
  font-size: 0.74rem;
}

.district-note {
  margin: 0;
  padding: 12px;
  border: 1px dashed rgba(148, 163, 184, 0.26);
  color: #94a3b8;
  border-radius: 12px;
  font-size: 0.86rem;
}

.support-empty {
  margin: 0;
  color: #94a3b8;
}

@media (max-width: 1200px) {
  .main-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 680px) {
  .seoul-page {
    padding: 18px 14px 36px;
  }

  .step-tabs {
    grid-template-columns: 1fr;
  }

  .map-shell {
    transform: none;
  }

  .seoul-map {
    min-height: 420px;
  }

  .support-stats {
    grid-template-columns: 1fr;
  }

  .population-grid {
    grid-template-columns: 1fr;
  }

  .policy-row {
    grid-template-columns: 1fr;
  }
}
</style>
