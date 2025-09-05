<template>
  <div class="data-view">
    <h1>環境データ表示</h1>
    
    <div class="filters">
      <div class="filter-group">
        <label for="location">場所:</label>
        <select id="location" v-model="filters.location" @change="fetchData">
          <option value="">すべての場所</option>
          <option v-for="location in locations" :key="location" :value="location">
            {{ location }}
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="start-date">開始日:</label>
        <input 
          id="start-date" 
          type="date" 
          v-model="filters.startDate" 
          @change="fetchData"
        >
      </div>
      
      <div class="filter-group">
        <label for="end-date">終了日:</label>
        <input 
          id="end-date" 
          type="date" 
          v-model="filters.endDate" 
          @change="fetchData"
        >
      </div>
    </div>
    
    <div v-if="loading" class="loading">データを読み込み中...</div>
    
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else-if="environmentalData.length === 0" class="no-data">
      データが見つかりません
    </div>
    
    <div v-else class="data-table">
      <table>
        <thead>
          <tr>
            <th>日付</th>
            <th>場所</th>
            <th>気温 (°C)</th>
            <th>湿度 (%)</th>
            <th>大気質指数</th>
            <th>CO2レベル (ppm)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="data in environmentalData" :key="data.id">
            <td>{{ formatDate(data.date) }}</td>
            <td>{{ data.location }}</td>
            <td>{{ data.temperature.toFixed(1) }}</td>
            <td>{{ data.humidity.toFixed(1) }}</td>
            <td>{{ data.air_quality_index }}</td>
            <td>{{ data.co2_level.toFixed(1) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="data-summary" v-if="environmentalData.length > 0">
      <p>表示件数: {{ environmentalData.length }}件</p>
    </div>
  </div>
</template>

<script>
import { environmentalDataAPI } from '../services/api'

export default {
  name: 'DataView',
  data() {
    return {
      environmentalData: [],
      locations: [],
      filters: {
        location: '',
        startDate: '',
        endDate: ''
      },
      loading: false,
      error: null
    }
  },
  async mounted() {
    await this.loadLocations()
    await this.fetchData()
  },
  methods: {
    async loadLocations() {
      try {
        const response = await environmentalDataAPI.getLocations()
        this.locations = response.data.locations
      } catch (error) {
        console.error('Failed to load locations:', error)
      }
    },
    
    async fetchData() {
      this.loading = true
      this.error = null
      
      try {
        const params = {}
        if (this.filters.location) params.location = this.filters.location
        if (this.filters.startDate) params.start_date = this.filters.startDate
        if (this.filters.endDate) params.end_date = this.filters.endDate
        
        const response = await environmentalDataAPI.getEnvironmentalData(params)
        this.environmentalData = response.data.data
      } catch (error) {
        this.error = 'データの取得に失敗しました'
        console.error('Failed to fetch data:', error)
      } finally {
        this.loading = false
      }
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ja-JP')
    }
  }
}
</script>

<style scoped>
.data-view {
  max-width: 100%;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: bold;
  color: #2c5530;
}

.filter-group select,
.filter-group input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.loading, .error, .no-data {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.error {
  color: #d32f2f;
}

.data-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background-color: #2c5530;
  color: white;
  padding: 1rem;
  text-align: left;
  font-weight: bold;
}

td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

tbody tr:hover {
  background-color: #f5f5f5;
}

.data-summary {
  margin-top: 1rem;
  text-align: center;
  color: #666;
}
</style>