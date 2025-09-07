<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        <h1>環境データ分析システム</h1>
      </div>
      <ul class="nav-menu">
        <li><router-link to="/">ホーム</router-link></li>
        <li><router-link to="/data">データ表示</router-link></li>
        <li><router-link to="/analysis">分析結果</router-link></li>
        <li><router-link to="/japan">🇯🇵 日本の環境問題</router-link></li>
      </ul>
    </nav>
    <main class="main-content">
      <router-view/>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
}

.navbar {
  background-color: #2c5530;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand h1 {
  font-size: 1.5rem;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 2rem;
}

.nav-menu a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-menu a:hover,
.nav-menu a.router-link-active {
  background-color: rgba(255, 255, 255, 0.1);
}

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}
</style>