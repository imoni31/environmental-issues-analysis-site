<template>
  <div class="home">
    <div class="hero-section">
      <h1>環境データ分析システムへようこそ</h1>
      <p>環境データの収集、分析、可視化を行うためのプラットフォームです</p>
    </div>
    
    <div class="features">
      <div class="feature-card">
        <h3>📊 データ表示</h3>
        <p>環境データをリアルタイムで表示し、フィルタリング機能で詳細な検索が可能です</p>
        <router-link to="/data" class="btn">データを見る</router-link>
      </div>
      
      <div class="feature-card">
        <h3>📈 分析結果</h3>
        <p>収集されたデータの統計情報とトレンド分析をグラフィカルに表示します</p>
        <router-link to="/analysis" class="btn">分析を見る</router-link>
      </div>
    </div>
    
    <div class="system-status" v-if="systemHealth">
      <h3>システム状況</h3>
      <div class="status-item">
        <span class="status-indicator healthy"></span>
        <span>システム正常動作中</span>
        <span class="timestamp">{{ systemHealth.timestamp }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { environmentalDataAPI } from '../services/api'

export default {
  name: 'Home',
  data() {
    return {
      systemHealth: null
    }
  },
  async mounted() {
    try {
      const response = await environmentalDataAPI.healthCheck()
      this.systemHealth = response.data
    } catch (error) {
      console.error('Health check failed:', error)
    }
  }
}
</script>

<style scoped>
.home {
  text-align: center;
}

.hero-section {
  background: linear-gradient(135deg, #2c5530, #4a7c59);
  color: white;
  padding: 4rem 2rem;
  border-radius: 12px;
  margin-bottom: 3rem;
}

.hero-section h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.hero-section p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  color: #2c5530;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  margin-bottom: 1.5rem;
}

.btn {
  display: inline-block;
  background-color: #2c5530;
  color: white;
  padding: 0.8rem 1.5rem;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #1e3a20;
}

.system-status {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.status-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  justify-content: center;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.status-indicator.healthy {
  background-color: #4caf50;
}

.timestamp {
  color: #666;
  font-size: 0.9rem;
}
</style>