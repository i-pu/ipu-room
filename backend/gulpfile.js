const gulp = require('gulp')
const uglify = require('gulp-uglify')
const babel = require('gulp-babel')
const plumber = require('gulp-plumber')
const rename = require('gulp-rename')
const typescript = require('gulp-typescript')

const tsProject = typescript.createProject('tsconfig.json', () => {
  typescript: require('typescript')
})

gulp.task('ts', () => {
  return gulp.src([
    './src/**/*.ts',
    '!./node_modules/**'
  ])
    .pipe(tsProject())
    .pipe(babel())
    .pipe(uglify())
    .pipe(gulp.dest('dist'))
})

gulp.task('uglify', () => {
  return gulp.src('dist/bundle.js')
    .pipe(plumber())
    .pipe(uglify())
    .pipe(rename({
      extname: '.min.js'
    }))
    .pipe(gulp.dest('dist'))
})

gulp.task('default', gulp.series('ts', 'uglify', done => {
  console.log('[Gulp] Task completed.')
  done()
}))