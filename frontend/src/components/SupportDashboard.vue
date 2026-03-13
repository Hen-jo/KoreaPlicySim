<template>
  <div class="support-dashboard" v-if="dashboard">
    <div class="dashboard-header">
      <div>
        <div class="eyebrow">캠페인 스코어보드</div>
        <h3>{{ dashboard.target_city }} {{ dashboard.race_type === 'seoul_mayor' ? '시장 선거 시나리오' : '캠페인 시나리오' }}</h3>
      </div>
      <div class="badge">{{ dashboard.target_districts?.join(', ') || '서울' }}</div>
    </div>

    <div class="action-summary" v-if="dashboard.campaign_action">
      <div class="action-type">{{ dashboard.campaign_action.action_type }}</div>
      <div class="action-text">{{ dashboard.campaign_action.summary }}</div>
    </div>

    <div class="candidate-grid" v-if="dashboard.candidates?.length">
      <div v-for="candidate in dashboard.candidates" :key="candidate.candidate_name" class="metric-card">
        <div class="metric-title">{{ candidate.candidate_name }} <span v-if="candidate.party">({{ candidate.party }})</span></div>
        <div class="metric-row"><span>지지율</span><strong>{{ candidate.citywide_approval_shift }}</strong></div>
        <div class="metric-row"><span>호감도</span><strong>{{ candidate.citywide_favorability_shift }}</strong></div>
        <div class="metric-row"><span>투표의향</span><strong>{{ candidate.citywide_vote_intent_shift }}</strong></div>
        <div class="metric-row"><span>스윙 유권자</span><strong>{{ candidate.citywide_swing_voter_shift }}</strong></div>
      </div>
    </div>

    <div class="table-block" v-if="dashboard.districts?.length">
      <div class="table-title">구별 변화 맵</div>
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>지역</th>
              <th>지지율</th>
              <th>투표의향</th>
              <th>스윙</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="district in dashboard.districts" :key="district.district">
              <td>{{ district.district }}</td>
              <td>{{ district.approval_shift }}</td>
              <td>{{ district.vote_intent_shift }}</td>
              <td>{{ district.swing_voter_shift }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="table-block" v-if="dashboard.blocs?.length">
      <div class="table-title">유권자 블록 반응</div>
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>블록</th>
              <th>지역</th>
              <th>투표의향</th>
              <th>반응</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="bloc in dashboard.blocs.slice(0, 8)" :key="`${bloc.district}-${bloc.bloc_key}`">
              <td>{{ bloc.bloc_label }}</td>
              <td>{{ bloc.district }}</td>
              <td>{{ bloc.vote_intent_shift }}</td>
              <td>{{ bloc.likely_reaction }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="drivers-row">
      <div class="driver-card">
        <div class="table-title">상승 요인</div>
        <ul><li v-for="item in dashboard.top_positive_drivers || []" :key="item">{{ item }}</li></ul>
      </div>
      <div class="driver-card">
        <div class="table-title">리스크 요인</div>
        <ul><li v-for="item in dashboard.top_negative_drivers || []" :key="item">{{ item }}</li></ul>
      </div>
    </div>

    <div class="uncertainty">{{ dashboard.uncertainty_note }}</div>
  </div>
</template>

<script setup>
defineProps({
  dashboard: {
    type: Object,
    default: null
  }
})
</script>

<style scoped>
.support-dashboard {
  border: 1px solid #e5e5e5;
  background: #fff;
  padding: 18px;
  margin-bottom: 18px;
}
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 12px;
  margin-bottom: 14px;
}
.eyebrow {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #666;
}
.dashboard-header h3 {
  margin: 4px 0 0;
  font-size: 18px;
}
.badge {
  font-size: 12px;
  border: 1px solid #111;
  padding: 6px 8px;
}
.action-summary {
  border-left: 3px solid #ff4500;
  padding-left: 10px;
  margin-bottom: 16px;
}
.action-type {
  font-size: 12px;
  text-transform: uppercase;
  color: #666;
}
.action-text {
  margin-top: 4px;
  font-size: 14px;
}
.candidate-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}
.metric-card {
  border: 1px solid #eaeaea;
  padding: 12px;
}
.metric-title {
  font-weight: 700;
  margin-bottom: 8px;
}
.metric-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding: 3px 0;
}
.table-block {
  margin-bottom: 16px;
}
.table-scroll {
  width: 100%;
  overflow-x: auto;
}
.table-title {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #666;
  margin-bottom: 8px;
}
table {
  width: 100%;
  min-width: 560px;
  border-collapse: collapse;
  font-size: 13px;
}
th, td {
  border-bottom: 1px solid #efefef;
  text-align: left;
  padding: 8px 6px;
  vertical-align: top;
}
.drivers-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.driver-card {
  border: 1px solid #eaeaea;
  padding: 12px;
}
.driver-card ul {
  margin: 0;
  padding-left: 18px;
}
.uncertainty {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid #eee;
  color: #666;
  font-size: 12px;
}

@media (max-width: 900px) {
  .dashboard-header,
  .drivers-row {
    grid-template-columns: 1fr;
    display: grid;
  }

  .dashboard-header {
    gap: 10px;
  }

  .badge {
    justify-self: start;
  }
}
</style>
