module.exports = {
  out: '../docs/backend',
  name: 'IPU-space Backend',
  readme: 'none',
  includes: './src/',
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