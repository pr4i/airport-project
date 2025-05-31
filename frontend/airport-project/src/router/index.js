import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import Flights from '@/views/Flights.vue'
import Dashboard from '@/views/Dashboard.vue'
import Register from '@/views/Register.vue'
import Home from '@/views/Home.vue'
import AdminPanel from '@/views/AdminPanel.vue'
import { useUserStore } from '@/stores/user'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/dashboard', component: Dashboard, name: 'Dashboard' },
  { path: '/flights', component: Flights, name: 'Flights' },
  { path: '/login', component: Login, name: 'Login' },
  { path: '/register', component: Register, name: 'Register' },
  { path: '/home', component: Home, name: 'Home' },
  { path: '/admin', component: AdminPanel, name: 'AdminPanel', meta: { requiresAdmin: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  const isAuth = !!userStore.token

  // Если есть токен, но профиль не загружен — загрузить профиль!
  if (isAuth && !userStore.userInfo) {
    try {
      await userStore.fetchProfile()
    } catch (e) {
      userStore.logout()
      return next('/home')
    }
  }

  const isAdmin = userStore.userInfo?.roles?.includes('admin')

  // ----- Гость -----
  if (!isAuth) {
    // Разрешено только на home, login, register
    if (['/home', '/login', '/register'].includes(to.path)) {
      return next()
    }
    return next('/home')
  }

  // ----- Запрещаем не-админу на /admin -----
  if (to.path === '/admin' && !isAdmin) {
    return next('/home')
  }

  // ----- Если залогинен и идёт на /login или /register — перебрасываем в dashboard -----
  if (to.path === '/login' || to.path === '/register') {
    return next('/dashboard')
  }

  // ----- Всё остальное разрешено -----
  return next()
})




export default router
