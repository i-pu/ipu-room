module.exports = {
  out: '../docs/client',
  name: 'IPU-space',
  readme: 'none',
  includes: './src/views/',
  exclude: [
    './node_modules/**/*',
    './tests/**/*',
    './yarn-cache/**/*'
  ],
  mode: 'file',
  excludeExternals: true,
  excludeNotExported: true,
  // excludePrivate: true
};