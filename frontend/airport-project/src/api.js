import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000', // обязательно порт backend, а не фронта!
})

// Добавляем токен авторизации к каждому запросу (если есть)
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
