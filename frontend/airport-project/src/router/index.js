import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Flights from '@/views/Flights.vue'
import Dashboard from '@/views/Dashboard.vue'
import Register from '@/views/Register.vue'
import Home from '@/views/Home.vue'

const routes = [
  { path: '/', component: Login, name: 'Login' },
  { path: '/dashboard', component: Dashboard, name: 'Dashboard' },
  { path: '/flights', component: Flights, name: 'Flights' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  {path: '/home', component: Home}
  
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
