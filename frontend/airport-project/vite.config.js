import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vuetify'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src', // Alias для src
      'vuetify': 'vuetify/dist/vuetify.js', // Убедитесь, что используете правильный путь для импорта Vuetify
    }
  }
})
