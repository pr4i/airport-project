import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Flights from '@/views/Flights.vue'
import Profile from '@/views/Profile.vue'
import About from '@/views/About.vue'
import Dashboard from '@/views/Dashboard.vue'

const routes = [
  { path: '/', component: Login, name: 'Login' },
  { path: '/dashboard', component: Dashboard, name: 'Dashboard' },
  { path: '/about', component: About, name: 'About' },
  { path: '/flights', component: Flights, name: 'Flights' },
  { path: '/profile', component: Profile, name: 'Profile' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
