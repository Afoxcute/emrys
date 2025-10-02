// Custom webpack configuration for Docker builds
// This completely bypasses chunking to prevent cache issues

const path = require('path');

module.exports = {
  mode: 'production',
  entry: './src/pages/_app.tsx',
  output: {
    path: path.resolve(__dirname, '.next/static/chunks'),
    filename: 'main.js',
    chunkFilename: 'main.js',
    publicPath: '/_next/static/chunks/',
  },
  optimization: {
    // Force everything into a single chunk
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        default: false,
        vendors: false,
        single: {
          name: 'main',
          chunks: 'all',
          enforce: true,
          priority: 1,
        },
      },
    },
    runtimeChunk: false,
    // Disable all optimizations that create chunks
    removeAvailableModules: false,
    removeEmptyChunks: false,
    usedExports: false,
    sideEffects: false,
    minimize: false,
    concatenateModules: false,
    // Force deterministic IDs
    moduleIds: 'deterministic',
    chunkIds: 'deterministic',
  },
  plugins: [
    // Force single chunk
    new (require('webpack')).optimize.LimitChunkCountPlugin({
      maxChunks: 1,
    }),
  ],
  resolve: {
    fallback: {
      fs: false,
      global: 'global',
      process: 'process/browser',
      buffer: 'buffer',
      util: 'util',
      stream: 'stream-browserify',
      crypto: 'crypto-browserify',
      vm: 'vm-browserify',
      os: 'os-browserify/browser',
      path: 'path-browserify',
    },
  },
  module: {
    rules: [
      {
        test: /\.m?js$/,
        resolve: {
          fullySpecified: false,
        },
      },
      {
        test: /node_modules\/@walletconnect\/.*\.js$/,
        type: 'javascript/auto',
        resolve: {
          fullySpecified: false,
        },
      },
      {
        test: /node_modules\/@solana\/wallet-adapter-walletconnect\/.*\.js$/,
        type: 'javascript/auto',
        resolve: {
          fullySpecified: false,
        },
      },
    ],
  },
};
