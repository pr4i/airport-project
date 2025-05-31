export default function mockCss() {
  return {
    name: 'mock-css',
    enforce: /** @type {'pre'} */ ('pre'),
    resolveId(source) {
      if (source.endsWith('.css')) return source
      return null
    },
    load(id) {
      if (id.endsWith('.css')) return ''
      return null
    }
  }
}
