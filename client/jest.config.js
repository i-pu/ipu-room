process.env.VUE_CLI_BABEL_TARGET_NODE = true
process.env.VUE_CLI_BABEL_TRANSPILE_MODULES = true

module.exports = {
  "moduleFileExtensions": [
    "js",
    "jsx",
    "json",
    "vue",
    "ts",
    "tsx"
  ],
  "transform": {
    "^.+\\.vue$": "vue-jest",
    ".+\\.(css|styl|less|sass|scss|svg|png|jpg|ttf|woff|woff2)$": "jest-transform-stub",
    "^.+\\.jsx?$": "babel-jest",
    "^.+\\.tsx?$": "ts-jest"
  },
  "transformIgnorePatterns": [
    "/node_modules/"
  ],
  "moduleNameMapper": {
    "^@/(.*)$": "<rootDir>/src/$1"
  },
  "snapshotSerializers": [
    "jest-serializer-vue"
  ],
  "testMatch": [
    "**/tests/unit/**/*.spec.(js|jsx|ts|tsx)|**/__tests__/*.(js|jsx|ts|tsx)"
  ],
  "testURL": "http://localhost/",
  "watchPlugins": [
    "jest-watch-typeahead/filename",
    "jest-watch-typeahead/testname"
  ],
  "globals": {
    "ts-jest": {
      "babelConfig": true
    }
  }
}