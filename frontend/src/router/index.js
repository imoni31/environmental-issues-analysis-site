import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import DataView from '../views/DataView.vue'
import Analysis from '../views/Analysis.vue'
import JapanEnvironmental from '../views/JapanEnvironmental.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/data',
    name: 'DataView',
    component: DataView
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: Analysis
  },
  {
    path: '/japan',
    name: 'JapanEnvironmental',
    component: JapanEnvironmental
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router