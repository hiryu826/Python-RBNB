const gulp = require("gulp");

const css = () => {
  const postCSS = require("gulp-postcss");
  const sass = require("gulp-sass");
  const minify = require("gulp-csso");
  sass.compiler = require("node-sass");
  return gulp
    .src("assets/scss/styles.scss") //경로
    .pipe(sass().on("error", sass.logError)) //sass로 작업하기 위해 sass로 pipe 한다.
    .pipe(postCSS([require("tailwindcss"), require("autoprefixer")])) //postCSS가 이해하는 플러그인
    .pipe(minify()) //모든 아웃풋을 minify 한다.
    .pipe(gulp.dest("static/css")); // 결과물을 static/css안에 넣는다.
};

exports.default = css;
