import { createRouter, createWebHistory } from 'vue-router'
import Flights from '@/views/Flights.vue'
import Profile from '@/views/Profile.vue'
import About from '@/views/About.vue'

const routes = [
  { path: '/', redirect: '/flights' },
  { path: '/about', component: About },
  { path: '/flights', component: Flights },
  { path: '/profile', component: Profile },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
