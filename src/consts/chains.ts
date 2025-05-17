import {
  eclipsemainnet,
  eclipsemainnetAddresses,
  evmos,
  evmosAddresses,
  solanadevnet,
  solanatestnetAddresses,
  sonicsvmtestnet,
  sonicsvmtestnetAddresses,
  soon,
  soonAddresses,
} from '@hyperlane-xyz/registry';
import { ChainMap, ChainMetadata } from '@hyperlane-xyz/sdk';
// import { ProtocolType } from '@hyperlane-xyz/utils';

// A map of chain names to ChainMetadata
// Chains can be defined here, in chains.json, or in chains.yaml
// Chains already in the SDK need not be included here unless you want to override some fields
// Schema here: https://github.com/hyperlane-xyz/hyperlane-monorepo/blob/main/typescript/sdk/src/metadata/chainMetadataTypes.ts
export const chains: ChainMap<ChainMetadata & { mailbox?: Address }> = {
  solanadevnet: {
    ...solanadevnet,
    // SVM chains require mailbox addresses for the token adapters
    mailbox: solanatestnetAddresses.mailbox,
  },
  eclipsemainnet: {
    ...eclipsemainnet,
    mailbox: eclipsemainnetAddresses.mailbox,
  },
  soon: {
    ...soon,
    mailbox: soonAddresses.mailbox,
  },
  sonicsvmtestnet: {
    ...sonicsvmtestnet,
    mailbox: sonicsvmtestnetAddresses.mailbox,
  },
  evmos: {
    ...evmos,
    mailbox: evmosAddresses.mailbox,
  },

  // eclipsetestnetv: {
  //   protocol: ProtocolType.Sealevel,
  //   chainId: 239092742,
  //   domainId: 239092742,
  //   name: 'eclipsetestnet',
  //   displayName: 'Eclipse Testnet',
  //   nativeToken: { name: 'Ether', symbol: 'ETH', decimals: 9 },
  //   rpcUrls: [{ http: 'https://testnet.dev2.eclipsenetwork.xyz' }],
  //   blockExplorers: [
  //     {
  //       name: 'MyCustomScan',
  //       url: 'https://explorer.dev.eclipsenetwork.xyz/?cluster=testnet',
  //       apiUrl: 'https://api.mycustomchain-scan.com/api',
  //       family: ExplorerFamily.Etherscan,
  //     },
  //   ],
  //   blocks: {
  //     confirmations: 1,
  //     reorgPeriod: 0,
  //     estimateBlockTime: 0.4,
  //   },
  //   logoURI: '/logo.svg',
  // },

  // mycustomchain: {
  //   protocol: ProtocolType.Ethereum,
  //   chainId: 123123,
  //   domainId: 123123,
  //   name: 'mycustomchain',
  //   displayName: 'My Chain',
  //   nativeToken: { name: 'Ether', symbol: 'ETH', decimals: 18 },
  //   rpcUrls: [{ http: 'https://mycustomchain-rpc.com' }],
  //   blockExplorers: [
  //     {
  //       name: 'MyCustomScan',
  //       url: 'https://mycustomchain-scan.com',
  //       apiUrl: 'https://api.mycustomchain-scan.com/api',
  //       family: ExplorerFamily.Etherscan,
  //     },
  //   ],
  //   blocks: {
  //     confirmations: 1,
  //     reorgPeriod: 1,
  //     estimateBlockTime: 10,
  //   },
  //   logoURI: '/logo.svg',
  // },
};
