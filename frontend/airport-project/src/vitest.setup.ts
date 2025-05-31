// src/vitest.setup.js

// Заглушка, чтобы избежать ошибок при импорте .css файлов в Vuetify
import { vi } from 'vitest'

vi.stubGlobal('CSSStyleSheet', class {})
