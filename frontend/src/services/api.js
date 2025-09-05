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

export default apiClient