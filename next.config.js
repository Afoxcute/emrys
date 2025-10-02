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
    env: {
      CF_PAGES_COMMIT_SHA: process.env.CF_PAGES_COMMIT_SHA,
    },
    webpack(config, options) {
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
