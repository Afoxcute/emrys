# Emrys - Cross-Chain Bridge and DeFi Platform

![Emrys Logo](/public/emrys-logo1.png)

Emrys is a cutting-edge cross-chain bridge that enables secure, fast token transfers between multiple blockchain networks. Built with a focus on performance, security, and user experience, Emrys leverages multiple innovative technologies to provide a seamless bridging experience.

## Core Technologies

### SOON SVM (Solana Virtual Machine)

Emrys utilizes a custom fork of the Solana Virtual Machine (SOON SVM) to provide:

- **High-throughput transaction processing**: Capable of handling thousands of transactions per second
- **Parallel transaction execution**: Enabling faster bridging operations compared to traditional bridges
- **Low-latency confirmations**: Reduces waiting times for users during cross-chain transfers
- **Robust smart contract execution**: Secure and reliable token locking and minting across chains

Our proprietary fork of SVM has been optimized specifically for cross-chain operations, enhancing the efficiency of token transfers while maintaining the security guarantees of the original Solana VM.

### IBC (Inter-Blockchain Communication)

The backbone of Emrys' cross-chain functionality is our implementation of the Inter-Blockchain Communication protocol:

- **Chain-agnostic messaging**: Standardized communication between heterogeneous blockchain networks
- **Light client verification**: Cryptographic validation of cross-chain messages
- **Trustless operation**: No central authority or validator set required for message relay
- **Protocol-level security**: Messages are cryptographically verified at the protocol level

Our IBC implementation enables seamless token transfers between EVM chains (Ethereum, Avalanche, Polygon, BSC) and Solana, with plans to expand to more ecosystems in the future.

### Walrus Decentralized Storage

Emrys integrates Walrus, a next-generation decentralized storage solution:

- **Immutable transaction records**: All cross-chain transactions are permanently stored
- **Distributed data fragments**: Transaction data is split and stored across multiple nodes
- **Rapid data retrieval**: Low-latency access to transaction history from any chain
- **Censorship resistance**: No single point of failure or control
- **Encryption**: Data is encrypted before being stored on the network

Walrus ensures that users always have access to their transaction history regardless of which blockchain they're using, enhancing transparency and auditability.

### fetch.ai uAgents

Our interactive FAQ and support system is powered by fetch.ai's uAgents technology:

- **Autonomous AI agents**: Intelligent responses to user queries
- **Context-aware conversations**: The system understands the context of questions
- **Multi-step reasoning**: Complex queries are broken down and resolved systematically
- **Domain-specific knowledge**: Deep understanding of blockchain, bridging, and Emrys-specific concepts
- **Continuous learning**: The system improves over time based on user interactions

## Bridge Implementation

### Mainnet Bridge

The mainnet bridge supports:

- Cross-chain transfers of native tokens and popular standards
- Token wrapping and unwrapping
- Fee optimization
- Relayer network for automated completions
- Gas estimation and fee transparency

Implementation leverages:
- SOON SVM for execution
- IBC for secure message passing
- Walrus for transaction record storage

### Testnet Bridge

The testnet implementation provides a safe environment for users to:

- Test native token bridging from EVM chains to Solana
- Experience the full bridging workflow without risking real assets
- Understand fee structures and timing expectations

Key features of the testnet:
- Supports all major EVM chains (Ethereum, Avalanche, Polygon, BSC)
- Dynamic native token detection (ETH, AVAX, MATIC, BNB)
- Transparent bridging process with step-by-step updates
- SOL as the destination token on Solana

### ZPL UTXO Bridge

The ZPL UTXO Bridge is a sophisticated cross-chain solution that enables secure and efficient movement of assets between UTXO-based blockchains (like Bitcoin, Dogecoin, and Litecoin) and Solana's account-based system. This comprehensive bridge implements a two-way peg mechanism allowing users to deposit, withdraw, and manage assets across fundamentally different blockchain architectures.

#### Key Features

- **Cross-Chain Asset Movement**: Deposit BTC/DOGE/LTC and receive wrapped assets (zBTC/zDOGE/zLTC) on Solana
- **Two-Way Peg**: Fully redeemable assets with bidirectional movement
- **Hot/Cold Reserve System**: Advanced security architecture for asset management
- **Multi-Wallet Support**: Integrates with various Bitcoin wallets
- **Multi-Cryptocurrency Support**: Works with Bitcoin, Dogecoin, and Litecoin
- **Portfolio Management**: Track and manage your cross-chain assets
- **Transaction History**: View and track all cross-chain operations

#### Technical Implementation

The UTXO Bridge implements sophisticated UTXO management:

- **UTXO Selection**: Intelligent selection of UTXOs for optimal transaction fees
- **Dust Management**: Proper handling of dust amounts to prevent stuck funds
- **Fee Estimation**: Dynamic fee calculation based on network conditions
- **P2TR Support**: Native support for Pay-to-Taproot addresses
- **Transaction Construction**: Building, signing, and broadcasting transactions

#### Security Model

- **Hot Reserve**: For regular deposit/withdrawal operations with time-locked scripts
- **Cold Reserve**: For secure long-term asset storage with recovery parameters
- **Guardian System**: Monitors and secures cross-chain operations
- **Time-Locked Scripts**: Provides security for user funds with specified unlock heights
- **IBC Module**: Handles inter-blockchain communication with light clients and packet verification

#### ZPL Client Functions

The ZPL (UTXO Layer Protocol) Client provides core functionality:

- **Reserve Management**: Managing hot and cold reserves for different cryptocurrencies
- **Account Services**: Creating and managing user accounts and positions
- **Instruction Construction**: Building Solana program instructions for all operations
- **Transaction Signing**: Handling transaction signing and submission
- **Position Tracking**: Monitoring user positions and balances

## Frontend Architecture

Emrys uses a modern React-based frontend with:

- Next.js for server-side rendering and routing
- TypeScript for type safety
- TailwindCSS for responsive design
- Formik for form handling
- React-toastify for notifications

## Security Features

- Chain connection monitoring
- Transaction verification
- OFAC compliance checks
- Multi-stage approval process
- Audit trail via Walrus storage

## Getting Started

### Prerequisites

- Node.js 16+
- Yarn 4.5.0+

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/emrys.git

# Navigate to the project directory
cd emrys

# Install dependencies
yarn install

# Start the development server
yarn dev
```

## UTXO Bridge Usage

### Deposit Flow

1. Connect your Bitcoin and Solana wallets
2. Select cryptocurrency type (BTC, DOGE, or LTC)
3. Enter the amount to deposit
4. Confirm the transaction in your wallet
5. Once confirmed on the source chain, funds will be credited as wrapped tokens on Solana

### Withdrawal Flow

1. Connect your wallets
2. Select cryptocurrency type
3. Enter the amount to withdraw
4. Choose a destination address
5. Confirm the transaction with your Solana wallet
6. Monitor the withdrawal status in the transaction history

## Documentation

For more detailed documentation on each component:

- [SOON SVM Documentation](docs/svm.md)
- [IBC Implementation Details](docs/ibc.md)
- [Walrus Storage Integration](docs/walrus.md)
- [Bridge Architecture](docs/bridge.md)
- [uAgents FAQ System](docs/uagents.md)
- [ZPL UTXO Bridge Documentation](docs/zpl-utxo.md)

## License

This project is licensed under the [License Name] - see the LICENSE file for details.

## Acknowledgments

- The Solana team for the original SVM implementation
- IBC Protocol developers
- fetch.ai for uAgents technology
- Bitcoin, Dogecoin, and Litecoin development communities
- All contributors and community members

---

***DISCLAIMER:*** *Emrys uses SVM & IBC & WALRUS for secure transactions & speed. All transactions are processed using our proprietary implementation of SVM (Solana Virtual Machine) and IBC (Inter-Blockchain Communication) protocols, with data secured through Walrus decentralized storage.*