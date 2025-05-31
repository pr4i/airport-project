// src/__mocks__/vite-css-hook.js
export default {
  name: 'mock-css',
  transform(code, id) {
    if (id.endsWith('.css')) return { code: '', map: null }
  }
}
