import { defineStore } from 'pinia'
import api from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token'),
    userInfo: null,           // { ... , role: "admin" или "user" }
  }),
  actions: {
    async login(username, password) {
      const res = await api.post('/auth/login', { username, password })
      this.token = res.data.access_token
      localStorage.setItem('token', this.token)
      api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      await this.fetchProfile() // загрузим userInfo с ролью
    },
    async fetchProfile() {
      const res = await api.get('/api/profile')
      this.userInfo = res.data // должен содержать поле "role"
    },
    logout() {
      this.token = null
      this.userInfo = null
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
    },
  },
  getters: {
   isAdmin: (state) => (state.userInfo && state.userInfo.roles?.includes('admin')),
    isUser: (state) => (state.userInfo && state.userInfo.roles?.includes('user'))
  }

})
