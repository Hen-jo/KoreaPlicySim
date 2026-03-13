<template>
  <div class="home-container">
    <!-- Top navigation -->
    <nav class="navbar">
      <div class="nav-brand">KOREAPOLICYSIM</div>
    </nav>

    <div class="main-content">
      <!-- Top half: Hero -->
      <section class="hero-section">
        <div class="hero-left">
          <div class="tag-row">
            <span class="orange-tag">서울 시장 선거운동 시뮬레이터</span>
            <span class="version-text">/ v0.1 preview</span>
          </div>
          
          <h1 class="main-title">
            공약문, 현안 브리프, 여론 메모를 올리고<br>
            <span class="gradient-text">서울 전역의 지지율 변화를 시뮬레이션하세요</span>
          </h1>
          
          <div class="hero-desc">
            <p>
              <span class="highlight-bold">KoreaPolicySim</span>은 짧은 문단 하나만 있어도 한국 정치 문서, 정책 초안, 선거 공약, 지역 현안을 바탕으로 시민 반응 환경을 시뮬레이션합니다. 상단 전략 보드에서 <span class="highlight-orange">서울 전체, 특정 구, 주요 유권자 블록</span>별로 지지, 불신, 호감도가 어떻게 움직일지 관찰할 수 있습니다.
            </p>
            <p class="slogan-text">
              도시가 반응하기 전에 선거 전략을 먼저 시험해보세요<span class="blinking-cursor">_</span>
            </p>
          </div>

          <div class="hero-brief">
            <div class="brief-card">
              <div class="brief-label">기본 선거</div>
              <div class="brief-value">서울시장 선거 또는 후보 미정 단계 모델링</div>
            </div>
            <div class="brief-card">
              <div class="brief-label">핵심 분석축</div>
              <div class="brief-value">구 단위 스윙 유권자 블록</div>
            </div>
            <div class="brief-card">
              <div class="brief-label">출력 지표</div>
              <div class="brief-value">지지율, 호감도, 투표의향</div>
            </div>
          </div>
           
          <div class="decoration-square"></div>
        </div>
        
        <div class="hero-right">
          <div class="hero-visual">
            <div class="visual-header">
              <span class="visual-kicker">서울 민심 보드</span>
              <span class="visual-badge">방향성 추정</span>
            </div>

            <div class="visual-grid">
              <div class="visual-panel scoreboard">
                <div class="panel-topline">정책 시그널</div>
                <div class="score-title">주거 + 교통 공약 발표 시나리오</div>
                <div class="signal-list">
                  <div class="signal-item">
                    <span>지지율</span>
                    <strong>+2 상승 압력</strong>
                  </div>
                  <div class="signal-item">
                    <span>핵심 스윙 구</span>
                    <strong>마포 / 관악</strong>
                  </div>
                  <div class="signal-item negative">
                    <span>리스크</span>
                    <strong>강남 형평성 역풍</strong>
                  </div>
                </div>
              </div>

              <div class="visual-panel map-card">
                <div class="panel-topline">구별 흐름</div>
                <div class="district-stack">
                  <div class="district-pill gain">
                    <span>관악</span>
                    <strong>+3</strong>
                  </div>
                  <div class="district-pill soft-gain">
                    <span>마포</span>
                    <strong>+2</strong>
                  </div>
                  <div class="district-pill flat">
                    <span>강남</span>
                    <strong>0 / 혼합</strong>
                  </div>
                </div>
              </div>

              <div class="visual-panel narrative-card">
                <div class="panel-topline">서사 확산</div>
                <div class="narrative-flow">
                  <span class="flow-node">캠프</span>
                  <span class="flow-arrow">→</span>
                  <span class="flow-node">방송</span>
                  <span class="flow-arrow">→</span>
                  <span class="flow-node">지역 대화</span>
                </div>
                <div class="narrative-note">
                  공약이 언론, 유권자 블록, 지역 이슈 네트워크를 거치며 어떻게 재해석되는지 추적합니다.
                </div>
              </div>
            </div>

            <div class="visual-overlay visual-overlay-one"></div>
            <div class="visual-overlay visual-overlay-two"></div>
          </div>
          
          <button class="scroll-down-btn" @click="scrollToBottom">
            ↓
          </button>
        </div>
      </section>

      <!-- Bottom half: two-column layout -->
      <section class="dashboard-section">
        <!-- Left column: status and steps -->
        <div class="left-panel">
          <div class="panel-header">
            <span class="status-dot">■</span> 시스템 상태
          </div>
          
          <h2 class="section-title">준비 완료</h2>
          <p class="section-desc">
            서울 정치 반응 엔진이 준비되어 있습니다. 정책 문서, 공약문, 구별 현안 브리프, 정치 해설을 올리면 서울 중심 시나리오를 바로 시작할 수 있습니다.
          </p>
          
          <!-- Metric cards -->
          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-value">구 단위 분석</div>
              <div class="metric-label">서울 각 구의 유권자 블록과 지역 현안을 함께 모델링</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">방향성 중심</div>
              <div class="metric-label">지지율, 호감도, 투표의향, 스윙 변화를 함께 추적</div>
            </div>
          </div>

          <!-- Workflow steps -->
          <div class="steps-container">
            <div class="steps-header">
               <span class="diamond-icon">◇</span> 워크플로
            </div>
            <div class="workflow-list">
              <div class="workflow-item">
                <span class="step-num">01</span>
                <div class="step-info">
                  <div class="step-title">그래프 구축</div>
                  <div class="step-desc">후보, 정당, 지역, 현안, 캠페인 관계를 정치 메모리 그래프로 정리합니다</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">02</span>
                <div class="step-info">
                  <div class="step-title">유권자 모델링</div>
                  <div class="step-desc">서울 유권자 블록, 이슈 민감도, 투표 성향, 구별 정치 감도를 생성합니다</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">03</span>
                <div class="step-info">
                  <div class="step-title">캠페인 실행</div>
                  <div class="step-desc">정책과 메시지가 유권자, 언론, 지역 서사를 따라 어떻게 퍼지는지 시뮬레이션합니다</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">04</span>
                <div class="step-info">
                  <div class="step-title">전략 보고서</div>
                  <div class="step-desc">구별 변화, 리스크, 지지 신호를 전략 메모 형태로 정리합니다</div>
                </div>
              </div>
              <div class="workflow-item">
                <span class="step-num">05</span>
                <div class="step-info">
                  <div class="step-title">워룸 Q&A</div>
                  <div class="step-desc">보고서를 검증하고 가정을 흔들어보며, 시뮬레이션된 유권자 블록과 직접 대화합니다</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right column: control console -->
        <div class="right-panel">
          <div class="console-box">
            <!-- Upload area -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">01 / Source Material</span>
                <span class="console-meta">지원 형식: PDF, MD, TXT</span>
              </div>
              
              <div 
                class="upload-zone"
                :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
                @dragover.prevent="handleDragOver"
                @dragleave.prevent="handleDragLeave"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
              >
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  accept=".pdf,.md,.txt"
                  @change="handleFileSelect"
                  style="display: none"
                  :disabled="loading"
                />
                
                <div v-if="files.length === 0" class="upload-placeholder">
                  <div class="upload-icon">↑</div>
                  <div class="upload-title">파일을 여기에 끌어오세요</div>
                  <div class="upload-hint">또는 클릭해서 문서를 선택하세요</div>
                </div>
                
                <div v-else class="file-list">
                  <div v-for="(file, index) in files" :key="index" class="file-item">
                    <span class="file-icon">📄</span>
                    <span class="file-name">{{ file.name }}</span>
                    <button @click.stop="removeFile(index)" class="remove-btn">×</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Divider -->
            <div class="console-divider">
              <span>Input Parameters</span>
            </div>

            <!-- Prompt area -->
            <div class="console-section">
              <div class="console-header">
                <span class="console-label">>_ 02 / 시뮬레이션 설명</span>
              </div>
              <div class="input-wrapper">
                <textarea
                  v-model="formData.simulationRequirement"
                  class="code-input"
                  placeholder="// 어떤 서울 정치 시나리오를 시험할지 적어주세요. 예: 주거비 부담이 서울 핵심 이슈가 될 때, 구별 지지율·투표의향·스윙 블록은 어떻게 움직이는가?"
                  rows="6"
                  :disabled="loading"
                ></textarea>
                <div class="model-note">현재 프리셋: 서울시장 선거 및 정책 반응 시뮬레이터</div>
                <div class="model-badge">Engine: KoreaPolicySim-V1.0</div>
              </div>
            </div>

            <div class="console-section">
              <div class="console-header">
                <span class="console-label">>_ 03 / 시나리오 조건</span>
              </div>
              <div class="input-wrapper">
                <div class="scenario-grid">
                  <input
                    v-model="formData.candidateName"
                    class="scenario-input"
                    placeholder="후보 이름 (선택)"
                    :disabled="loading"
                  />
                  <input
                    v-model="formData.candidateParty"
                    class="scenario-input"
                    placeholder="정당 또는 연합 (선택)"
                    :disabled="loading"
                  />
                  <input
                    v-model="formData.candidateSlogan"
                    class="scenario-input"
                    placeholder="캠페인 메시지 또는 슬로건 (선택)"
                    :disabled="loading"
                  />
                  <input
                    v-model="formData.targetDistrictsText"
                    class="scenario-input"
                    placeholder="대상 구, 쉼표로 구분 (비우면 서울 전체)"
                    :disabled="loading"
                  />
                </div>
                <textarea
                  v-model="formData.campaignActionBrief"
                  class="code-input compact"
                  placeholder="// 정책 변화나 캠페인 신호를 적어주세요. 예: 주거비 문제가 서울 핵심 의제가 되고, 구별 언론 프레이밍이 갈리며, 임차인들이 형평성과 실현 가능성을 두고 논쟁한다."
                  rows="4"
                  :disabled="loading"
                ></textarea>
              </div>
            </div>

            <!-- Start button -->
            <div class="console-section btn-section">
              <button 
                class="start-engine-btn"
                @click="startSimulation"
                :disabled="!canSubmit || loading"
              >
                <span v-if="!loading">서울 유권자 모델 만들기</span>
                <span v-else>초기화 중...</span>
                <span class="btn-arrow">→</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Historical projects -->
      <HistoryDatabase />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'

const router = useRouter()

// 表单数据
const formData = ref({
  simulationRequirement: '',
  simulationPreset: 'korea_society_policy',
  candidateName: '',
  candidateParty: '',
  candidateSlogan: '',
  targetDistrictsText: 'Gangnam, Mapo, Gwanak',
  campaignActionBrief: ''
})

// 文件列表
const files = ref([])

// 状态
const loading = ref(false)
const error = ref('')
const isDragOver = ref(false)

// 文件输入引用
const fileInput = ref(null)

// 计算属性:是否可以提交
const canSubmit = computed(() => {
  return (
    formData.value.simulationRequirement.trim() !== '' &&
    formData.value.campaignActionBrief.trim() !== '' &&
    files.value.length > 0
  )
})

// 触发文件选择
const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

// 处理文件选择
const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

// 处理拖拽相关
const handleDragOver = (e) => {
  if (!loading.value) {
    isDragOver.value = true
  }
}

const handleDragLeave = (e) => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  
  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

// 添加文件
const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt'].includes(ext)
  })
  files.value.push(...validFiles)
}

// 移除文件
const removeFile = (index) => {
  files.value.splice(index, 1)
}

// 滚动到底部
const scrollToBottom = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'
  })
}

// 开始模拟 - 立即跳转，API调用在Process页面进行
const startSimulation = () => {
  if (!canSubmit.value || loading.value) return
  
  // 存储待上传的数据
  import('../store/pendingUpload.js').then(({ setPendingUpload }) => {
    setPendingUpload(
      files.value,
      formData.value.simulationRequirement,
      formData.value.simulationPreset,
      {
        raceType: 'seoul_mayor',
        targetCity: 'Seoul',
        targetDistricts: formData.value.targetDistrictsText
          .split(',')
          .map(item => item.trim())
          .filter(Boolean),
        candidateProfiles: formData.value.candidateName.trim()
          ? [{
              name: formData.value.candidateName.trim(),
              party: formData.value.candidateParty.trim(),
              slogan: formData.value.candidateSlogan.trim()
            }]
          : [],
        campaignActionBrief: formData.value.campaignActionBrief.trim()
      }
    )
    
    // 立即跳转到Process页面（使用特殊标识表示新建项目）
    router.push({
      name: 'Process',
      params: { projectId: 'new' }
    })
  })
}
</script>

<style scoped>
/* 全局变量与重置 */
:root {
  --black: #000000;
  --white: #FFFFFF;
  --orange: #FF4500;
  --gray-light: #F5F5F5;
  --gray-text: #666666;
  --border: #E5E5E5;
  /* 
    使用 Space Grotesk 作为主要标题字体，JetBrains Mono 作为代码/标签字体
    确保已在 index.html 引入这些 Google Fonts 
  */
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  --font-cn: 'Noto Sans SC', system-ui, sans-serif;
}

.home-container {
  min-height: 100vh;
  background:
    radial-gradient(circle at top right, rgba(255, 69, 0, 0.1), transparent 28%),
    linear-gradient(180deg, #fffdf9 0%, #ffffff 32%, #faf7f2 100%);
  font-family: var(--font-sans);
  color: var(--black);
}

/* 顶部导航 */
.navbar {
  height: 60px;
  background: var(--black);
  color: var(--white);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.nav-brand {
  font-family: var(--font-mono);
  font-weight: 800;
  letter-spacing: 1px;
  font-size: 1.2rem;
}

.nav-links {
  display: flex;
  align-items: center;
}

.github-link {
  color: var(--white);
  text-decoration: none;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: opacity 0.2s;
}

.github-link:hover {
  opacity: 0.8;
}

.arrow {
  font-family: sans-serif;
}

/* 主要内容区 */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Hero 区域 */
.hero-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 80px;
  position: relative;
  align-items: stretch;
  gap: 48px;
}

.hero-left {
  flex: 1;
  padding-right: 60px;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}

.orange-tag {
  background: var(--orange);
  color: var(--white);
  padding: 4px 10px;
  font-weight: 700;
  letter-spacing: 1px;
  font-size: 0.75rem;
}

.version-text {
  color: #999;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.main-title {
  font-size: 4.5rem;
  line-height: 1.2;
  font-weight: 600;
  margin: 0 0 32px 0;
  letter-spacing: -2px;
  color: var(--black);
  max-width: 780px;
}

.gradient-text {
  background: linear-gradient(90deg, #111111 0%, #ff4500 80%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.hero-desc {
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--gray-text);
  max-width: 640px;
  margin-bottom: 50px;
  font-weight: 400;
  text-align: justify;
}

.hero-desc p {
  margin-bottom: 1.5rem;
}

.highlight-bold {
  color: var(--black);
  font-weight: 700;
}

.highlight-orange {
  color: var(--orange);
  font-weight: 700;
  font-family: var(--font-mono);
}

.highlight-code {
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 2px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--black);
  font-weight: 600;
}

.slogan-text {
  font-size: 1.2rem;
  font-weight: 520;
  color: var(--black);
  letter-spacing: 1px;
  border-left: 3px solid var(--orange);
  padding-left: 15px;
  margin-top: 20px;
}

.hero-brief {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  max-width: 760px;
  margin-bottom: 32px;
}

.brief-card {
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: blur(8px);
  padding: 16px 18px;
}

.brief-label {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: #777;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 8px;
}

.brief-value {
  font-size: 0.98rem;
  font-weight: 600;
  color: #111;
  line-height: 1.4;
}

.blinking-cursor {
  color: var(--orange);
  animation: blink 1s step-end infinite;
  font-weight: 700;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.decoration-square {
  width: 16px;
  height: 16px;
  background: var(--orange);
}

.hero-right {
  flex: 0.8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
}

.hero-visual {
  width: 100%;
  min-height: 520px;
  padding: 28px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.96), rgba(247, 241, 233, 0.96)),
    linear-gradient(180deg, rgba(255, 69, 0, 0.08), transparent);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08);
}

.visual-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  position: relative;
  z-index: 1;
}

.visual-kicker {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: #555;
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

.visual-badge {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: #fff;
  background: #111;
  padding: 7px 10px;
  letter-spacing: 0.06em;
}

.visual-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.9fr;
  grid-template-rows: auto auto;
  gap: 16px;
  margin-top: 18px;
  position: relative;
  z-index: 1;
}

.visual-panel {
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.82);
  padding: 18px;
  backdrop-filter: blur(6px);
}

.scoreboard {
  grid-row: 1 / span 2;
}

.panel-topline {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: #777;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 14px;
}

.score-title {
  font-size: 1.6rem;
  line-height: 1.2;
  font-weight: 700;
  color: #111;
  max-width: 280px;
  margin-bottom: 22px;
}

.signal-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.signal-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  font-size: 0.9rem;
}

.signal-item strong {
  font-family: var(--font-mono);
  font-size: 0.84rem;
  color: #111;
}

.signal-item.negative strong {
  color: #b63d00;
}

.district-stack {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.district-pill {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 14px;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.district-pill.gain {
  background: linear-gradient(90deg, rgba(255, 112, 67, 0.2), rgba(255,255,255,0.9));
}

.district-pill.soft-gain {
  background: linear-gradient(90deg, rgba(255, 184, 77, 0.18), rgba(255,255,255,0.9));
}

.district-pill.flat {
  background: linear-gradient(90deg, rgba(0, 0, 0, 0.05), rgba(255,255,255,0.95));
}

.narrative-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.narrative-flow {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 18px;
}

.flow-node {
  font-family: var(--font-mono);
  font-size: 0.82rem;
  padding: 8px 10px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.92);
}

.flow-arrow {
  color: var(--orange);
  font-weight: 700;
}

.narrative-note {
  font-size: 0.9rem;
  line-height: 1.6;
  color: #555;
}

.visual-overlay {
  position: absolute;
  border-radius: 999px;
  filter: blur(10px);
  opacity: 0.7;
}

.visual-overlay-one {
  width: 180px;
  height: 180px;
  background: rgba(255, 69, 0, 0.14);
  top: -30px;
  right: -20px;
}

.visual-overlay-two {
  width: 120px;
  height: 120px;
  background: rgba(255, 193, 7, 0.12);
  bottom: 20px;
  right: 60px;
}

.scroll-down-btn {
  width: 40px;
  height: 40px;
  border: 1px solid var(--border);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--orange);
  font-size: 1.2rem;
  transition: all 0.2s;
}

.scroll-down-btn:hover {
  border-color: var(--orange);
}

/* Dashboard 双栏布局 */
.dashboard-section {
  display: flex;
  gap: 60px;
  border-top: 1px solid var(--border);
  padding-top: 60px;
  align-items: flex-start;
}

.dashboard-section .left-panel,
.dashboard-section .right-panel {
  display: flex;
  flex-direction: column;
}

/* 左侧面板 */
.left-panel {
  flex: 0.8;
}

.panel-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.status-dot {
  color: var(--orange);
  font-size: 0.8rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 520;
  margin: 0 0 15px 0;
}

.section-desc {
  color: var(--gray-text);
  margin-bottom: 25px;
  line-height: 1.6;
}

.metrics-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.metric-card {
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.8);
  padding: 20px 30px;
  min-width: 150px;
}

.metric-value {
  font-family: var(--font-mono);
  font-size: 1.8rem;
  font-weight: 520;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 0.85rem;
  color: #999;
}

/* 项目模拟步骤介绍 */
.steps-container {
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.75);
  padding: 30px;
  position: relative;
}

.steps-header {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.diamond-icon {
  font-size: 1.2rem;
  line-height: 1;
}

.workflow-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.step-num {
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--black);
  opacity: 0.3;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 520;
  font-size: 1rem;
  margin-bottom: 4px;
}

.step-desc {
  font-size: 0.85rem;
  color: var(--gray-text);
}

/* 右侧交互控制台 */
.right-panel {
  flex: 1.2;
}

.console-box {
  border: 1px solid rgba(0, 0, 0, 0.12);
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.07);
  padding: 8px;
}

.console-section {
  padding: 20px;
}

.console-section.btn-section {
  padding-top: 0;
}

.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #666;
}

.upload-zone {
  border: 1px dashed #CCC;
  height: 200px;
  overflow-y: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #FAFAFA;
}

.upload-zone.has-files {
  align-items: flex-start;
}

.upload-zone:hover {
  background: #F0F0F0;
  border-color: #999;
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  width: 40px;
  height: 40px;
  border: 1px solid #DDD;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: #999;
}

.upload-title {
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.upload-hint {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: #999;
}

.file-list {
  width: 100%;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  display: flex;
  align-items: center;
  background: var(--white);
  padding: 8px 12px;
  border: 1px solid #EEE;
  font-family: var(--font-mono);
  font-size: 0.85rem;
}

.file-name {
  flex: 1;
  margin: 0 10px;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #999;
}

.console-divider {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.console-divider::before,
.console-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #EEE;
}

.console-divider span {
  padding: 0 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #BBB;
  letter-spacing: 1px;
}

.input-wrapper {
  position: relative;
  border: 1px solid #DDD;
  background: #FAFAFA;
}

.scenario-grid {
  display: grid;
  gap: 12px;
  margin-bottom: 12px;
}

.scenario-input {
  width: 100%;
  border: 1px solid #DDD;
  background: #FFF;
  padding: 12px 14px;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  line-height: 1.5;
  outline: none;
}

.scenario-input:focus {
  border-color: var(--orange);
}

.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 20px;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  min-height: 150px;
}

.code-input.compact {
  min-height: 110px;
}

.model-badge {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #AAA;
}

.model-note {
  position: absolute;
  bottom: 10px;
  left: 15px;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: #777;
}

.start-engine-btn {
  width: 100%;
  background: var(--black);
  color: var(--white);
  border: none;
  padding: 20px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 1.1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
}

/* 可点击状态（非禁用） */
.start-engine-btn:not(:disabled) {
  background: var(--black);
  border: 1px solid var(--black);
  animation: pulse-border 2s infinite;
}

.start-engine-btn:hover:not(:disabled) {
  background: var(--orange);
  border-color: var(--orange);
  transform: translateY(-2px);
}

.start-engine-btn:active:not(:disabled) {
  transform: translateY(0);
}

.start-engine-btn:disabled {
  background: #E5E5E5;
  color: #999;
  cursor: not-allowed;
  transform: none;
  border: 1px solid #E5E5E5;
}

/* 引导动画：微妙的边框脉冲 */
@keyframes pulse-border {
  0% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.2); }
  70% { box-shadow: 0 0 0 6px rgba(0, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0); }
}

/* 响应式适配 */
@media (max-width: 1024px) {
  .dashboard-section {
    flex-direction: column;
  }
  
  .hero-section {
    flex-direction: column;
  }
  
  .hero-left {
    padding-right: 0;
    margin-bottom: 40px;
  }

  .hero-brief {
    grid-template-columns: 1fr;
  }

  .hero-visual {
    min-height: auto;
  }

  .visual-grid {
    grid-template-columns: 1fr;
  }

  .scoreboard {
    grid-row: auto;
  }
}
</style>
