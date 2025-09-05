<template>
  <div class="analysis">
    <h1>環境データ分析</h1>
    
    <div v-if="loading" class="loading">分析データを読み込み中...</div>
    
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else class="analysis-content">
      <div class="stats-grid">
        <div class="stat-card">
          <h3>気温統計</h3>
          <div class="stat-values">
            <div class="stat-item">
              <span class="label">平均:</span>
              <span class="value">{{ statistics.temperature?.avg?.toFixed(1) }}°C</span>
            </div>
            <div class="stat-item">
              <span class="label">最低:</span>
              <span class="value">{{ statistics.temperature?.min?.toFixed(1) }}°C</span>
            </div>
            <div class="stat-item">
              <span class="label">最高:</span>
              <span class="value">{{ statistics.temperature?.max?.toFixed(1) }}°C</span>
            </div>
          </div>
        </div>
        
        <div class="stat-card">
          <h3>湿度統計</h3>
          <div class="stat-values">
            <div class="stat-item">
              <span class="label">平均:</span>
              <span class="value">{{ statistics.humidity?.avg?.toFixed(1) }}%</span>
            </div>
            <div class="stat-item">
              <span class="label">最低:</span>
              <span class="value">{{ statistics.humidity?.min?.toFixed(1) }}%</span>
            </div>
            <div class="stat-item">
              <span class="label">最高:</span>
              <span class="value">{{ statistics.humidity?.max?.toFixed(1) }}%</span>
            </div>
          </div>
        </div>
        
        <div class="stat-card">
          <h3>大気質指数統計</h3>
          <div class="stat-values">
            <div class="stat-item">
              <span class="label">平均:</span>
              <span class="value">{{ Math.round(statistics.air_quality_index?.avg || 0) }}</span>
            </div>
            <div class="stat-item">
              <span class="label">最低:</span>
              <span class="value">{{ statistics.air_quality_index?.min }}</span>
            </div>
            <div class="stat-item">
              <span class="label">最高:</span>
              <span class="value">{{ statistics.air_quality_index?.max }}</span>
            </div>
          </div>
        </div>
        
        <div class="stat-card">
          <h3>CO2レベル統計</h3>
          <div class="stat-values">
            <div class="stat-item">
              <span class="label">平均:</span>
              <span class="value">{{ statistics.co2_level?.avg?.toFixed(1) }}ppm</span>
            </div>
            <div class="stat-item">
              <span class="label">最低:</span>
              <span class="value">{{ statistics.co2_level?.min?.toFixed(1) }}ppm</span>
            </div>
            <div class="stat-item">
              <span class="label">最高:</span>
              <span class="value">{{ statistics.co2_level?.max?.toFixed(1) }}ppm</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="analysis-insights">
        <h2>分析結果</h2>
        <div class="insights-grid">
          <div class="insight-card">
            <h4>気温状況</h4>
            <p>{{ getTemperatureInsight() }}</p>
          </div>
          <div class="insight-card">
            <h4>大気質状況</h4>
            <p>{{ getAirQualityInsight() }}</p>
          </div>
          <div class="insight-card">
            <h4>CO2レベル状況</h4>
            <p>{{ getCO2Insight() }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { environmentalDataAPI } from '../services/api'

export default {
  name: 'Analysis',
  data() {
    return {
      statistics: {},
      loading: false,
      error: null
    }
  },
  async mounted() {
    await this.fetchStatistics()
  },
  methods: {
    async fetchStatistics() {
      this.loading = true
      this.error = null
      
      try {
        const response = await environmentalDataAPI.getStatistics()
        this.statistics = response.data.statistics
      } catch (error) {
        this.error = '統計データの取得に失敗しました'
        console.error('Failed to fetch statistics:', error)
      } finally {
        this.loading = false
      }
    },
    
    getTemperatureInsight() {
      const temp = this.statistics.temperature
      if (!temp) return '分析中...'
      
      if (temp.avg > 20) {
        return '平均気温が高めです。暑い気候が続いています。'
      } else if (temp.avg < 10) {
        return '平均気温が低めです。寒い気候が続いています。'
      } else {
        return '平均気温は適度な範囲にあります。'
      }
    },
    
    getAirQualityInsight() {
      const aqi = this.statistics.air_quality_index
      if (!aqi) return '分析中...'
      
      if (aqi.avg > 50) {
        return '大気質指数が高めです。大気汚染に注意が必要です。'
      } else if (aqi.avg < 25) {
        return '大気質指数は良好です。きれいな空気環境です。'
      } else {
        return '大気質指数は中程度です。通常の範囲内です。'
      }
    },
    
    getCO2Insight() {
      const co2 = this.statistics.co2_level
      if (!co2) return '分析中...'
      
      if (co2.avg > 450) {
        return 'CO2レベルが高めです。換気や環境改善を検討してください。'
      } else if (co2.avg < 400) {
        return 'CO2レベルは良好です。健康的な環境です。'
      } else {
        return 'CO2レベルは通常の範囲内です。'
      }
    }
  }
}
</script>

<style scoped>
.analysis {
  max-width: 100%;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.error {
  color: #d32f2f;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.stat-card h3 {
  color: #2c5530;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.stat-values {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  color: #666;
}

.value {
  font-weight: bold;
  color: #2c5530;
}

.analysis-insights {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.analysis-insights h2 {
  color: #2c5530;
  margin-bottom: 1.5rem;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.insight-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #2c5530;
}

.insight-card h4 {
  color: #2c5530;
  margin-bottom: 0.5rem;
}

.insight-card p {
  color: #666;
  line-height: 1.6;
}
</style>