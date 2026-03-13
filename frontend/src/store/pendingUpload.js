/**
 * 临时存储待上传的文件和需求
 * 用于首页点击启动引擎后立即跳转，在Process页面再进行API调用
 */
import { reactive } from 'vue'

const state = reactive({
  files: [],
  simulationRequirement: '',
  simulationPreset: 'korea_society_policy',
  raceType: 'seoul_mayor',
  targetCity: 'Seoul',
  targetDistricts: [],
  candidateProfiles: [],
  campaignActionBrief: '',
  isPending: false
})

export function setPendingUpload(files, requirement, preset = 'korea_society_policy', scenario = {}) {
  state.files = files
  state.simulationRequirement = requirement
  state.simulationPreset = preset
  state.raceType = scenario.raceType || 'seoul_mayor'
  state.targetCity = scenario.targetCity || 'Seoul'
  state.targetDistricts = scenario.targetDistricts || []
  state.candidateProfiles = scenario.candidateProfiles || []
  state.campaignActionBrief = scenario.campaignActionBrief || ''
  state.isPending = true
}

export function getPendingUpload() {
  return {
    files: state.files,
    simulationRequirement: state.simulationRequirement,
    simulationPreset: state.simulationPreset,
    raceType: state.raceType,
    targetCity: state.targetCity,
    targetDistricts: state.targetDistricts,
    candidateProfiles: state.candidateProfiles,
    campaignActionBrief: state.campaignActionBrief,
    isPending: state.isPending
  }
}

export function clearPendingUpload() {
  state.files = []
  state.simulationRequirement = ''
  state.simulationPreset = 'korea_society_policy'
  state.raceType = 'seoul_mayor'
  state.targetCity = 'Seoul'
  state.targetDistricts = []
  state.candidateProfiles = []
  state.campaignActionBrief = ''
  state.isPending = false
}

export default state
