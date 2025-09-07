import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const environmentalDataAPI = {
  getEnvironmentalData(params = {}) {
    return apiClient.get('/environmental-data', { params })
  },

  getStatistics() {
    return apiClient.get('/environmental-data/statistics')
  },

  getLocations() {
    return apiClient.get('/locations')
  },

  healthCheck() {
    return apiClient.get('/health')
  }
}

// 日本の環境問題データ用の新しいAPI
export const japanEnvironmentalAPI = {
  getAirQuality(prefecture = 'Tokyo') {
    return apiClient.get('/japan/air-quality', { params: { prefecture } })
  },

  getClimateData() {
    return apiClient.get('/japan/climate')
  },

  getPollutionData() {
    return apiClient.get('/japan/pollution')
  },

  getBiodiversityData() {
    return apiClient.get('/japan/biodiversity')
  },

  getEnergyEmissions() {
    return apiClient.get('/japan/energy-emissions')
  },

  getComprehensiveReport() {
    return apiClient.get('/japan/comprehensive-report')
  },

  getEnvironmentalProblems() {
    return apiClient.get('/japan/environmental-problems')
  }
}

export default apiClient