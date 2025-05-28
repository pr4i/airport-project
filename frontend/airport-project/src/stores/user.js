import { defineStore } from 'pinia'
import api from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: null,
    userInfo: null,
  }),
  actions: {
    async login(username, password) {
      const res = await api.post('/auth/login', { username, password })
      this.token = res.data.access_token
      api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      await this.fetchProfile()
    },
    async fetchProfile() {
      const res = await api.get('/api/profile')
      this.userInfo = res.data
    },
    logout() {
      this.token = null
      this.userInfo = null
      delete api.defaults.headers.common['Authorization']
    },
  },
})
