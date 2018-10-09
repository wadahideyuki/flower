// gulpプラグインの読み込み
var gulp = require('gulp');
// エラーによる停止を防止するプラグインの読み込み
var plumber = require('gulp-plumber');
// デスクトップ通知のプラグインの読み込み
var notify = require('gulp-notify');
// Sassをコンパイルするプラグインの読み込み
var sass = require('gulp-sass');
// mediaqueryをまとめる
var cmq = require('gulp-combine-media-queries');
// パグ
var pug = require('gulp-pug');
// ブラウザシンク
var browserSync = require('browser-sync');
//画像の圧縮
var changed  = require('gulp-changed');
var imagemin = require('gulp-imagemin');
var imageminJpg = require('imagemin-jpeg-recompress');
var imageminPng = require('imagemin-pngquant');
var imageminGif = require('imagemin-gifsicle');
var svgmin = require('gulp-svgmin');



// パスの設定
var paths = {
    cssDir : 'common/css',
    scssDir : 'src/common/css',
    srcDir : 'src/assets/images',
    dstDir : 'assets/images'
}

// jpg,png,gif画像の圧縮タスク
gulp.task('imagemin', function(){
  console.log("gazou")
    var srcGlob = paths.srcDir + '/**/*.+(jpg|jpeg|png|gif)';
    var dstGlob = paths.dstDir;
    gulp.src( srcGlob )
    .pipe(changed( dstGlob ))
    .pipe(imagemin([
        imageminPng(),
        imageminJpg(),
        imageminGif({
            interlaced: false,
            optimizationLevel: 3,
            colors:180
        })
    ]
    ))
    .pipe(gulp.dest( dstGlob ));
});
// svg画像の圧縮タスク
gulp.task('svgmin', function(){
    var srcGlob = paths.srcDir + '/**/*.+(svg)';
    var dstGlob = paths.dstDir;
    gulp.src( srcGlob )
    .pipe(changed( dstGlob ))
    .pipe(svgmin())
    .pipe(gulp.dest( dstGlob ));
});

// scssのコンパイル
gulp.task("sass", function(){
  console.log("sass")
	// .scssファイルを取得
	gulp.src([paths.scssDir + '/**/*.scss'])
	// エラーでも止まらないように
	.pipe(plumber({
		// エラーをデスクトップ通知
		errorHandler: notify.onError({
			message: "ふぁいる→ <%= error.message %>",
			title: "えらー",
			icon: "error.png"
		})
	}))
	// Sassのコンパイルを実行
	.pipe(sass({outputStyle: 'expanded'})
	// Sassのコンパイルエラーを表示
	// (これがないと自動的に止まってしまう)
	.on('error', sass.logError))
	// cssフォルダー以下に保存
	.pipe(gulp.dest(paths.cssDir))
	// 完了をデスクトップ通知
//	.pipe(notify({
//		title: "scssコンパイル完了→ <%= file.relative %>",
//		message: new Date(),
//		sound: "Glass"
//	}));
});

// メディアクエリをまとめる
gulp.task("cmq", function(){
	gulp.src([paths.cssDir + '/**/*.css'])
	.pipe(cmq({
		log: false
	}))
	.pipe(gulp.dest(paths.cssDir))
	// 完了をデスクトップ通知
//	.pipe(notify({
//		title: "MQまとめ完了→ <%= file.relative %>",
//		message: new Date(),
//		sound: "Glass"
//	}));
});

// パグ
gulp.task("pug", () => {
	return gulp.src(["src/**/*.pug", "!" + "src/**/_*.pug"], {base: "src"})
	.pipe(plumber({
		errorHandler: notify.onError({
			message: "ふぁいる→ <%= error.message %>",
			title: "えらー",
			icon: "error.png"
		})
	}))
	.pipe(pug({
		basedir: "src",
		pretty: true
	}))
	.pipe(gulp.dest("./"));
});



// ブラウザシンク
gulp.task("browser-sync", function(){
	browserSync({
		server:{
			baseDir: "./",
			index: "index.html"
		}
	});
});

// ブラウザリロード
gulp.task("bs-reload", function(){
	browserSync.reload();
});

// ★ ファイルを監視
gulp.task("watch", function(){
	gulp.watch(['src/**/*.pug'], ["pug", "bs-reload"]);
	gulp.watch(paths.scssDir + '/**/*.scss', ["sass", "bs-reload"]);
//	gulp.watch(paths.cssDir + '/**/*.css', ["cmq", "bs-reload"]);
	gulp.watch('./*.html', ["browser-sync", "bs-reload"]);
  gulp.watch(paths.srcDir + '/**/*', ['imagemin','svgmin']);
  console.log("gazou")
});

// npx gulpで実行
gulp.task('default', ["browser-sync", "watch"]);
