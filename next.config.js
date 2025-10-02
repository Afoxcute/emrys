const { version } = require('./package.json');
const { withSentryConfig } = require('@sentry/nextjs');
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

const borsh = require('@coral-xyz/borsh');
const { Connection, PublicKey } = require('@solana/web3.js');

const isDev = process.env.NODE_ENV !== 'production';

const ENABLE_CSP_HEADER = true;
const FRAME_SRC_HOSTS = [
  'https://*.walletconnect.com',
  'https://*.walletconnect.org',
  'https://cdn.solflare.com',
];
const STYLE_SRC_HOSTS = [];
const IMG_SRC_HOSTS = [
  'https://*.walletconnect.com',
  'https://*.githubusercontent.com',
  'https://cdn.jsdelivr.net/gh/hyperlane-xyz/hyperlane-registry@main/',
];

const cspHeader = `
  default-src 'self';
  script-src 'self'${isDev ? " 'unsafe-eval'" : ''};
  style-src 'self' 'unsafe-inline' ${STYLE_SRC_HOSTS.join(' ')};
  connect-src *;
  img-src 'self' blob: data: ${IMG_SRC_HOSTS.join(' ')};
  font-src 'self' data:;
  object-src 'none';
  base-uri 'self';
  form-action 'self';
  frame-src 'self' ${FRAME_SRC_HOSTS.join(' ')};
  frame-ancestors 'none';
  ${!isDev ? 'block-all-mixed-content;' : ''}
  ${!isDev ? 'upgrade-insecure-requests;' : ''}
`
  .replace(/\s{2,}/g, ' ')
  .trim();

const securityHeaders = [
  {
    key: 'X-XSS-Protection',
    value: '1; mode=block',
  },
  {
    key: 'X-Frame-Options',
    value: 'DENY',
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin',
  },
  ...(ENABLE_CSP_HEADER
    ? [
        {
          key: 'Content-Security-Policy',
          value: cspHeader,
        },
      ]
    : []),
];

// === Solana Bootstrap Code ===

const bootstrapSchema = borsh.struct([
  borsh.publicKey('superOperatorCertificate'),
  borsh.publicKey('chadbufferProgramId'),
  borsh.publicKey('bitcoinSpvProgramId'),
  borsh.publicKey('twoWayPegProgramId'),
  borsh.publicKey('liquidityManagementProgramId'),
  borsh.publicKey('delegatorProgramId'),
  borsh.publicKey('layerCaProgramId'),
]);

const guardianSettingSchema = borsh.struct([
  borsh.u32('seed'),
  borsh.publicKey('guardianCertificate'),
  borsh.publicKey('assetMint'),
  borsh.publicKey('tokenProgramId'),
  borsh.publicKey('splTokenMintAuthority'),
  borsh.publicKey('splTokenBurnAuthority'),
]);

async function getZplProgramIds(boostrapperProgramId, connection) {
  const bootstrapAccounts = await connection.getProgramAccounts(
    new PublicKey(boostrapperProgramId),
  );
  const bootstrapData = bootstrapSchema.decode(bootstrapAccounts[0].account.data);

  return {
    twoWayPegProgramId: bootstrapData.twoWayPegProgramId.toBase58(),
    liquidityManagementProgramId: bootstrapData.liquidityManagementProgramId.toBase58(),
    delegatorProgramId: bootstrapData.delegatorProgramId.toBase58(),
    bitcoinSpvProgramId: bootstrapData.bitcoinSpvProgramId.toBase58(),
    layerCaProgramId: bootstrapData.layerCaProgramId.toBase58(),
  };
}

async function getAssetMint(guardianSettingAccountAddress, connection) {
  const accountInfo = await connection.getAccountInfo(new PublicKey(guardianSettingAccountAddress));

  const data = guardianSettingSchema.decode(accountInfo.data.subarray(8));
  return data.assetMint.toBase58();
}

// === Async Config ===

const createNextConfig = async () => {
  // Fallback values for when Solana network is unavailable
  const fallbackProgramIds = {
    twoWayPegProgramId: '11111111111111111111111111111111',
    liquidityManagementProgramId: '11111111111111111111111111111111',
    delegatorProgramId: '11111111111111111111111111111111',
    layerCaProgramId: '11111111111111111111111111111111',
    bitcoinSpvProgramId: '11111111111111111111111111111111',
  };
  
  const fallbackAssetMint = '11111111111111111111111111111111';

  let programIds = fallbackProgramIds;
  let regtestAssetMint = fallbackAssetMint;
  let devnetBootstrapperProgramId = process.env.NEXT_PUBLIC_DEVNET_BOOTSTRAPPER_PROGRAM_ID || '11111111111111111111111111111111';

  try {
    const devnetConnection = new Connection(
      process.env.SOLANA_DEVNET_RPC || 'https://api.devnet.solana.com',
    );

    if (devnetBootstrapperProgramId) {
      programIds = await getZplProgramIds(devnetBootstrapperProgramId, devnetConnection);
    }

    if (process.env.NEXT_PUBLIC_REGTEST_DEVNET_TWO_WAY_PEG_GUARDIAN_SETTING) {
      regtestAssetMint = await getAssetMint(
        process.env.NEXT_PUBLIC_REGTEST_DEVNET_TWO_WAY_PEG_GUARDIAN_SETTING,
        devnetConnection,
      );
    }
  } catch (error) {
    console.warn('Failed to fetch Solana network data, using fallback values:', error.message);
  }

  const {
    twoWayPegProgramId,
    liquidityManagementProgramId,
    delegatorProgramId,
    layerCaProgramId,
    bitcoinSpvProgramId,
  } = programIds;

  const baseConfig = {
    reactStrictMode: true,
    output: 'standalone',
    generateEtags: false,
    poweredByHeader: false,
    // Optimize build performance
    experimental: {
      // Disable some expensive features during build
      optimizeCss: false,
      // Reduce memory usage
      memoryBasedWorkersCount: true,
    },
    // Skip trailing slash redirects
    skipTrailingSlashRedirect: true,
    // Disable static generation if specified
    ...(process.env.NEXT_DISABLE_STATIC_GENERATION === 'true' && {
      output: 'standalone',
      trailingSlash: false,
      images: {
        unoptimized: true,
      },
    }),
    env: {
      CF_PAGES_COMMIT_SHA: process.env.CF_PAGES_COMMIT_SHA,
    },
    webpack(config, options) {

      // Disable webpack cache for Docker builds
      config.cache = false;
      
      // Disable persistent caching
      if (config.cache && config.cache.type) {
        config.cache = false;
      }

      // More aggressive cache disabling for Docker
      if (process.env.NODE_ENV === 'production') {
        config.cache = false;
        delete config.cache;
        
        // Disable all webpack caching mechanisms
        config.snapshot = {
          managedPaths: [],
          immutablePaths: [],
          buildDependencies: {
            hash: false,
            timestamp: false,
          },
          module: {
            timestamp: false,
          },
          resolve: {
            timestamp: false,
          },
          resolveBuildDependencies: {
            hash: false,
            timestamp: false,
          },
        };

        // Disable chunking at the webpack level
        config.optimization = {
          ...config.optimization,
          splitChunks: false,
          runtimeChunk: false,
          moduleIds: 'deterministic',
          chunkIds: 'deterministic',
        };
      }

      config.module.rules.push({
        test: /\.ya?ml$/,
        use: 'yaml-loader',
      });

      if (options.nextRuntime === 'edge') {
        config.resolve.fallback = {
          ...config.resolve.fallback,
          crypto: 'crypto-browserify',
        };
      }

      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      };

      // Only add polyfills for client-side builds
      if (!options.isServer) {
        config.resolve.fallback = {
          ...config.resolve.fallback,
          global: 'global',
          process: 'process/browser',
          buffer: 'buffer',
          util: 'util',
          stream: 'stream-browserify',
          crypto: 'crypto-browserify',
          vm: 'vm-browserify',
          os: 'os-browserify/browser',
          path: 'path-browserify',
        };

        config.plugins = config.plugins || [];
        config.plugins.push(
          new (require('webpack')).ProvidePlugin({
            process: 'process/browser',
            Buffer: ['buffer', 'Buffer'],
            global: 'global',
          })
        );

        config.plugins.push(
          new (require('webpack')).DefinePlugin({
            'self': 'globalThis',
            'window': 'globalThis',
          })
        );
      }

      // Disable chunking optimizations that cause cache issues
      config.optimization = {
        ...config.optimization,
        splitChunks: false,
        runtimeChunk: false,
        // Reduce build time
        removeAvailableModules: false,
        removeEmptyChunks: false,
        usedExports: false,
        sideEffects: false,
        // Disable expensive optimizations
        minimize: false,
        concatenateModules: false,
        // Force deterministic IDs
        moduleIds: 'deterministic',
        chunkIds: 'deterministic',
      };

      // Handle ESM modules properly
      config.module.rules.push({
        test: /\.m?js$/,
        resolve: {
          fullySpecified: false,
        },
      });

      // Add specific handling for problematic ESM modules
      config.resolve.alias = {
        ...config.resolve.alias,
      };

      // Handle ESM modules in CommonJS context
      config.module.rules.push({
        test: /node_modules\/@walletconnect\/.*\.js$/,
        type: 'javascript/auto',
        resolve: {
          fullySpecified: false,
        },
      });

      // Handle Solana wallet adapter ESM imports
      config.module.rules.push({
        test: /node_modules\/@solana\/wallet-adapter-walletconnect\/.*\.js$/,
        type: 'javascript/auto',
        resolve: {
          fullySpecified: false,
        },
      });

      // Add comprehensive ESM support
      config.resolve.conditionNames = ['import', 'module', 'browser', 'default'];
      config.resolve.mainFields = ['browser', 'module', 'main'];

      // Add a custom loader for ESM modules that need special handling
      config.module.rules.push({
        test: /node_modules\/@solana\/wallet-adapter-walletconnect\/lib\/esm\/index\.js$/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
            plugins: [
              ['@babel/plugin-transform-modules-commonjs', { strict: false }]
            ]
          }
        }
      });

      // Ensure proper module resolution for ESM
      config.resolve.extensionAlias = {
        '.js': ['.js', '.ts', '.tsx'],
        '.mjs': ['.mjs', '.js'],
      };

      // Add ESM support for server-side rendering
      config.experiments = {
        ...config.experiments,
        topLevelAwait: true,
        asyncWebAssembly: true,
      };

      // Handle ESM imports in CommonJS context
      config.plugins = config.plugins || [];
      config.plugins.push(
        new (require('webpack')).DefinePlugin({
          'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
        })
      );


      return config;
    },
    async headers() {
      return [
        {
          source: '/(.*)',
          headers: securityHeaders,
        },
      ];
    },
    typescript: { ignoreBuildErrors: true },
    eslint: { ignoreDuringBuilds: true },
  };

  if (process.env.GITHUB_ACTIONS) {
    return baseConfig;
  }

  const nextConfig = {
    ...baseConfig,
    env: {
      ...baseConfig.env,
      NEXT_PUBLIC_VERSION: version,
      NEXT_PUBLIC_DEVNET_BOOTSTRAPPER_PROGRAM_ID: devnetBootstrapperProgramId,
      NEXT_PUBLIC_DEVNET_TWO_WAY_PEG_PROGRAM_ID: twoWayPegProgramId,
      NEXT_PUBLIC_DEVNET_LIQUIDITY_MANAGEMENT_PROGRAM_ID: liquidityManagementProgramId,
      NEXT_PUBLIC_DEVNET_DELEGATOR_PROGRAM_ID: delegatorProgramId,
      NEXT_PUBLIC_DEVNET_LAYER_CA_PROGRAM_ID: layerCaProgramId,
      NEXT_PUBLIC_DEVNET_BITCOIN_SPV_PROGRAM_ID: bitcoinSpvProgramId,
      NEXT_PUBLIC_REGTEST_ASSET_MINT: regtestAssetMint,
    },
  };

  const sentryOptions = {
    org: 'hyperlane',
    project: 'warp-ui',
    authToken: process.env.SENTRY_AUTH_TOKEN,
    hideSourceMaps: true,
    tunnelRoute: '/monitoring-tunnel',
    bundleSizeOptimizations: {
      excludeDebugStatements: true,
      excludeReplayIframe: true,
      excludeReplayShadowDom: true,
    },
  };

  return withBundleAnalyzer(withSentryConfig(nextConfig, sentryOptions));
};

module.exports = createNextConfig();
