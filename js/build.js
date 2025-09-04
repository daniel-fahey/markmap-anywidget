const esbuild = require('esbuild');
const path = require('path');

const isWatch = process.argv.includes('--watch');

const buildOptions = {
  entryPoints: ['widget.js'],
  outfile: path.join(__dirname, '../src/markmap_anywidget/static/widget.js'),
  bundle: true,
  minify: !isWatch, // Don't minify in watch mode for easier debugging
  format: 'esm',
  target: 'es2015',
  logLevel: 'info',
  // Bundle all dependencies for offline use
  external: [],
  // Handle all asset types
  loader: {
    '.css': 'text',
    '.woff': 'dataurl',
    '.woff2': 'dataurl',
    '.ttf': 'dataurl',
    '.eot': 'dataurl',
    '.svg': 'dataurl',
    '.png': 'dataurl',
    '.jpg': 'dataurl',
    '.jpeg': 'dataurl',
    '.gif': 'dataurl',
  },
  // Platform agnostic
  platform: 'browser',
  // Source maps for debugging
  sourcemap: !isWatch,
  // Ensure proper resolution
  absWorkingDir: __dirname,
};



async function build() {
  if (isWatch) {
    // Watch mode
    const ctx = await esbuild.context(buildOptions);
    await ctx.watch();
    console.log('👁️  Watching for changes...');
  } else {
    // Build mode
    await esbuild.build(buildOptions);
    console.log('✅ Build complete');
  }
}

build().catch((err) => {
  console.error(err);
  process.exit(1);
});
