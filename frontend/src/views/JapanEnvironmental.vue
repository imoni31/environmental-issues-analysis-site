<template>
  <div class="japan-environmental">
    <div class="page-header">
      <h1>🇯🇵 日本の環境問題データ</h1>
      <p>実際のデータに基づく日本の環境問題の現状と分析</p>
    </div>

    <!-- 環境問題概要 -->
    <div class="environmental-problems-section" v-if="environmentalProblems">
      <h2>主要な環境問題</h2>
      <div class="problems-grid">
        <div 
          v-for="problem in environmentalProblems.major_issues" 
          :key="problem.issue"
          class="problem-card"
          :class="getSeverityClass(problem.severity)"
        >
          <div class="problem-header">
            <h3>{{ problem.issue }}</h3>
            <span class="severity-badge" :class="problem.severity">{{ getSeverityText(problem.severity) }}</span>
          </div>
          <p class="problem-description">{{ problem.description }}</p>
          <div class="problem-details">
            <div class="affected-areas">
              <strong>影響地域:</strong> {{ problem.affected_areas.join(', ') }}
            </div>
            <div class="trend" :class="problem.trend">
              <strong>傾向:</strong> {{ getTrendText(problem.trend) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- データカテゴリ選択 -->
    <div class="data-categories">
      <h2>データカテゴリ</h2>
      <div class="category-buttons">
        <button 
          v-for="category in dataCategories" 
          :key="category.key"
          @click="selectCategory(category.key)"
          :class="{ active: selectedCategory === category.key }"
          class="category-btn"
        >
          {{ category.icon }} {{ category.name }}
        </button>
      </div>
    </div>

    <!-- ローディング状態 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>{{ selectedCategory }}データを読み込み中...</p>
    </div>

    <!-- エラー表示 -->
    <div v-else-if="error" class="error">
      <p>❌ {{ error }}</p>
      <button @click="loadCategoryData" class="retry-btn">再試行</button>
    </div>

    <!-- データ表示エリア -->
    <div v-else-if="currentData.length > 0" class="data-display">
      <!-- 大気質データ -->
      <div v-if="selectedCategory === 'airQuality'" class="air-quality-data">
        <h3>🌫️ 大気質データ</h3>
        <div class="prefecture-selector">
          <label for="prefecture">都道府県:</label>
          <select id="prefecture" v-model="selectedPrefecture" @change="loadAirQualityData">
            <option value="Tokyo">東京</option>
            <option value="Osaka">大阪</option>
            <option value="Nagoya">名古屋</option>
            <option value="Fukuoka">福岡</option>
            <option value="Sapporo">札幌</option>
          </select>
        </div>
        <div class="data-table">
          <table>
            <thead>
              <tr>
                <th>日付</th>
                <th>場所</th>
                <th>汚染物質</th>
                <th>濃度</th>
                <th>単位</th>
                <th>データ源</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in currentData" :key="item.date + item.parameter">
                <td>{{ formatDate(item.date) }}</td>
                <td>{{ item.location }}</td>
                <td>{{ item.parameter }}</td>
                <td>{{ item.value }}</td>
                <td>{{ item.unit }}</td>
                <td>{{ item.source }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 気候変動データ -->
      <div v-else-if="selectedCategory === 'climate'" class="climate-data">
        <h3>🌡️ 気候変動データ</h3>
        <div class="climate-grid">
          <div v-for="item in currentData.slice(0, 10)" :key="item.date" class="climate-card">
            <div class="date">{{ formatDate(item.date) }}</div>
            <div class="temperature-anomaly" :class="getTemperatureClass(item.temperature_anomaly)">
              気温偏差: {{ item.temperature_anomaly }}°C
            </div>
            <div class="average-temp">平均気温: {{ item.average_temperature }}°C</div>
            <div class="precipitation">降水量変化: {{ item.precipitation_change }}%</div>
            <div class="extreme-events">異常気象: {{ item.extreme_weather_events }}件</div>
          </div>
        </div>
      </div>

      <!-- 汚染データ -->
      <div v-else-if="selectedCategory === 'pollution'" class="pollution-data">
        <h3>🏭 汚染データ</h3>
        <div class="pollution-grid">
          <div v-for="item in currentData" :key="item.location" class="pollution-card">
            <h4>{{ item.location }}</h4>
            <div class="pollution-metrics">
              <div class="metric">
                <span class="label">工業排出:</span>
                <span class="value">{{ item.industrial_emissions }}</span>
              </div>
              <div class="metric">
                <span class="label">水質汚染指数:</span>
                <span class="value">{{ item.water_pollution_index }}</span>
              </div>
              <div class="metric">
                <span class="label">土壌汚染サイト:</span>
                <span class="value">{{ item.soil_contamination_sites }}箇所</span>
              </div>
              <div class="metric">
                <span class="label">廃棄物生成:</span>
                <span class="value">{{ item.waste_generation_tons }}トン</span>
              </div>
              <div class="metric">
                <span class="label">リサイクル率:</span>
                <span class="value">{{ item.recycling_rate }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 生物多様性データ -->
      <div v-else-if="selectedCategory === 'biodiversity'" class="biodiversity-data">
        <h3>🌿 生物多様性データ</h3>
        <div class="biodiversity-grid">
          <div v-for="item in currentData" :key="item.region" class="biodiversity-card">
            <h4>{{ item.region }}</h4>
            <div class="biodiversity-metrics">
              <div class="metric">
                <span class="label">森林被覆率:</span>
                <span class="value forest-coverage">{{ item.forest_coverage_percent }}%</span>
              </div>
              <div class="metric">
                <span class="label">年間森林減少率:</span>
                <span class="value deforestation">{{ item.deforestation_rate_annual }}%</span>
              </div>
              <div class="metric">
                <span class="label">絶滅危惧種:</span>
                <span class="value endangered">{{ item.endangered_species_count }}種</span>
              </div>
              <div class="metric">
                <span class="label">保護区域:</span>
                <span class="value">{{ item.protected_areas_hectares }}ha</span>
              </div>
              <div class="metric">
                <span class="label">外来種報告:</span>
                <span class="value">{{ item.invasive_species_reports }}件</span>
              </div>
              <div v-if="item.coral_bleaching_percent > 0" class="metric">
                <span class="label">サンゴ白化率:</span>
                <span class="value coral-bleaching">{{ item.coral_bleaching_percent }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- エネルギー・排出データ -->
      <div v-else-if="selectedCategory === 'energy'" class="energy-data">
        <h3>⚡ エネルギー・CO2排出データ</h3>
        <div class="energy-grid">
          <div v-for="item in currentData" :key="item.energy_source || item.date" class="energy-card">
            <h4>{{ item.energy_source }}</h4>
            <div class="energy-metrics">
              <div v-if="item.generation_percentage" class="metric">
                <span class="label">発電比率:</span>
                <span class="value">{{ item.generation_percentage }}%</span>
              </div>
              <div v-if="item.annual_generation_twh" class="metric">
                <span class="label">年間発電量:</span>
                <span class="value">{{ item.annual_generation_twh }}TWh</span>
              </div>
              <div v-if="item.co2_emissions_mt" class="metric">
                <span class="label">CO2排出量:</span>
                <span class="value">{{ item.co2_emissions_mt }}Mt</span>
              </div>
              <div v-if="item.total_co2_emissions_mt" class="metric">
                <span class="label">総CO2排出量:</span>
                <span class="value total-emissions">{{ item.total_co2_emissions_mt }}Mt</span>
              </div>
              <div v-if="item.renewable_energy_ratio" class="metric">
                <span class="label">再生可能エネルギー比率:</span>
                <span class="value renewable">{{ item.renewable_energy_ratio }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- データが無い場合 -->
    <div v-else class="no-data">
      <p>📊 データを表示するカテゴリを選択してください</p>
    </div>

    <!-- 政府の取り組み -->
    <div class="government-initiatives" v-if="environmentalProblems">
      <h2>政府の取り組み</h2>
      <div class="initiatives-list">
        <div v-for="initiative in environmentalProblems.government_initiatives" :key="initiative" class="initiative-item">
          ✅ {{ initiative }}
        </div>
      </div>
    </div>

    <!-- 国際的な取り組み -->
    <div class="international-commitments" v-if="environmentalProblems">
      <h2>国際的な取り組み</h2>
      <div class="commitments-list">
        <div v-for="commitment in environmentalProblems.international_commitments" :key="commitment" class="commitment-item">
          🌍 {{ commitment }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { japanEnvironmentalAPI } from '../services/api'

export default {
  name: 'JapanEnvironmental',
  data() {
    return {
      environmentalProblems: null,
      selectedCategory: '',
      selectedPrefecture: 'Tokyo',
      currentData: [],
      loading: false,
      error: null,
      dataCategories: [
        { key: 'airQuality', name: '大気質', icon: '🌫️' },
        { key: 'climate', name: '気候変動', icon: '🌡️' },
        { key: 'pollution', name: '汚染', icon: '🏭' },
        { key: 'biodiversity', name: '生物多様性', icon: '🌿' },
        { key: 'energy', name: 'エネルギー・排出', icon: '⚡' }
      ]
    }
  },
  async mounted() {
    await this.loadEnvironmentalProblems()
  },
  methods: {
    async loadEnvironmentalProblems() {
      try {
        const response = await japanEnvironmentalAPI.getEnvironmentalProblems()
        this.environmentalProblems = response.data.data
      } catch (error) {
        console.error('Failed to load environmental problems:', error)
      }
    },

    async selectCategory(category) {
      this.selectedCategory = category
      this.currentData = []
      await this.loadCategoryData()
    },

    async loadCategoryData() {
      this.loading = true
      this.error = null

      try {
        let response
        switch (this.selectedCategory) {
          case 'airQuality':
            response = await japanEnvironmentalAPI.getAirQuality(this.selectedPrefecture)
            break
          case 'climate':
            response = await japanEnvironmentalAPI.getClimateData()
            break
          case 'pollution':
            response = await japanEnvironmentalAPI.getPollutionData()
            break
          case 'biodiversity':
            response = await japanEnvironmentalAPI.getBiodiversityData()
            break
          case 'energy':
            response = await japanEnvironmentalAPI.getEnergyEmissions()
            break
          default:
            return
        }

        this.currentData = response.data.data || []
      } catch (error) {
        this.error = `${this.selectedCategory}データの取得に失敗しました`
        console.error('Failed to load category data:', error)
      } finally {
        this.loading = false
      }
    },

    async loadAirQualityData() {
      if (this.selectedCategory === 'airQuality') {
        await this.loadCategoryData()
      }
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ja-JP')
    },

    getSeverityClass(severity) {
      return `severity-${severity}`
    },

    getSeverityText(severity) {
      const severityMap = {
        'critical': '重大',
        'high': '高',
        'medium': '中',
        'low': '低'
      }
      return severityMap[severity] || severity
    },

    getTrendText(trend) {
      const trendMap = {
        'worsening': '悪化',
        'improving': '改善',
        'stable': '安定'
      }
      return trendMap[trend] || trend
    },

    getTemperatureClass(anomaly) {
      if (anomaly > 1) return 'hot'
      if (anomaly < -1) return 'cold'
      return 'normal'
    }
  }
}
</script>

<style scoped>
.japan-environmental {
  max-width: 100%;
  padding: 0;
}

.page-header {
  background: linear-gradient(135deg, #1b5e20, #2e7d32, #43a047);
  color: white;
  padding: 3rem 2rem;
  border-radius: 12px;
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.page-header p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.environmental-problems-section {
  margin-bottom: 3rem;
}

.environmental-problems-section h2 {
  color: #1b5e20;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.problems-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.problem-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  border-left: 6px solid;
  transition: transform 0.3s ease;
}

.problem-card:hover {
  transform: translateY(-5px);
}

.problem-card.severity-critical {
  border-left-color: #d32f2f;
}

.problem-card.severity-high {
  border-left-color: #f57c00;
}

.problem-card.severity-medium {
  border-left-color: #fbc02d;
}

.problem-card.severity-low {
  border-left-color: #388e3c;
}

.problem-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.problem-header h3 {
  color: #1b5e20;
  margin: 0;
}

.severity-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  color: white;
}

.severity-badge.critical {
  background-color: #d32f2f;
}

.severity-badge.high {
  background-color: #f57c00;
}

.severity-badge.medium {
  background-color: #fbc02d;
}

.severity-badge.low {
  background-color: #388e3c;
}

.problem-description {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.problem-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.affected-areas {
  color: #555;
}

.trend {
  font-weight: bold;
}

.trend.improving {
  color: #388e3c;
}

.trend.worsening {
  color: #d32f2f;
}

.trend.stable {
  color: #f57c00;
}

.data-categories {
  margin-bottom: 2rem;
}

.data-categories h2 {
  color: #1b5e20;
  margin-bottom: 1rem;
}

.category-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.category-btn {
  background: white;
  border: 2px solid #e0e0e0;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.category-btn:hover {
  border-color: #43a047;
  background-color: #f1f8e9;
}

.category-btn.active {
  background-color: #43a047;
  border-color: #43a047;
  color: white;
}

.loading {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e0e0e0;
  border-top: 4px solid #43a047;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  background: #ffebee;
  border: 1px solid #e57373;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  color: #c62828;
}

.retry-btn {
  background: #43a047;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
}

.data-display {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.prefecture-selector {
  margin-bottom: 1.5rem;
}

.prefecture-selector label {
  margin-right: 0.5rem;
  font-weight: bold;
  color: #1b5e20;
}

.prefecture-selector select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.data-table {
  overflow-x: auto;
}

.data-table table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.data-table th {
  background-color: #43a047;
  color: white;
  padding: 1rem;
  text-align: left;
  font-weight: bold;
}

.data-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #eee;
}

.data-table tbody tr:hover {
  background-color: #f5f5f5;
}

.climate-grid, .pollution-grid, .biodiversity-grid, .energy-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.climate-card, .pollution-card, .biodiversity-card, .energy-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  border-left: 4px solid #43a047;
}

.climate-card .date {
  font-weight: bold;
  color: #1b5e20;
  margin-bottom: 0.5rem;
}

.temperature-anomaly.hot {
  color: #d32f2f;
  font-weight: bold;
}

.temperature-anomaly.cold {
  color: #1976d2;
  font-weight: bold;
}

.temperature-anomaly.normal {
  color: #388e3c;
}

.pollution-metrics, .biodiversity-metrics, .energy-metrics {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.25rem 0;
}

.metric .label {
  color: #666;
  font-weight: 500;
}

.metric .value {
  font-weight: bold;
  color: #1b5e20;
}

.value.forest-coverage {
  color: #2e7d32;
}

.value.deforestation {
  color: #d32f2f;
}

.value.endangered {
  color: #f57c00;
}

.value.coral-bleaching {
  color: #e91e63;
}

.value.total-emissions {
  color: #d32f2f;
  font-size: 1.1em;
}

.value.renewable {
  color: #388e3c;
  font-size: 1.1em;
}

.no-data {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  color: #666;
  font-size: 1.2rem;
}

.government-initiatives, .international-commitments {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.government-initiatives h2, .international-commitments h2 {
  color: #1b5e20;
  margin-bottom: 1.5rem;
}

.initiatives-list, .commitments-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.initiative-item, .commitment-item {
  background: #f1f8e9;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #43a047;
}
</style>