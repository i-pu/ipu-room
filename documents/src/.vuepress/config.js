module.exports = {
  title: 'Ipu-room Document',
  description: 'APIの仕様等をまとめる',
  base: '.',
  dest: '../docs',
  themeConfig: {
    displayAllHeaders: true,
    sidebar: [
      '/',
      '/api/room-api.md',
      '/api/plugin-api.md',
      '/api/store-api.md',
      '/api/compiler-api.md',
      '/ci-cd/',
      '/client/',
      '/plugin/',
      '/spec/'
    ],
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Repos', link: 'https://github.com/i-pu/ipu-room' }
    ]
  }
}