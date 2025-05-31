import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import { fileURLToPath, URL } from 'url'

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      // ⬇️ добавляем заглушку .css файлов
      '\\.css$': fileURLToPath(new URL('./src/__mocks__/styleMock.js', import.meta.url))
    },
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue']
  },
  root: fileURLToPath(new URL('./', import.meta.url)),
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/vitest.setup.ts',
    mockReset: true,
    exclude: ['node_modules', 'dist', '**/node_modules/**']
  }
})
