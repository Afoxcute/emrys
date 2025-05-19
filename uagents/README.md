# Emrys Blockchain Technology Assistant uAgent

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)

## Overview

This directory contains the implementation of an AI-powered educational uAgent built using the fetch.ai uAgents framework. The uAgent serves as an interactive assistant that provides comprehensive information about the blockchain technologies used in the Emrys ecosystem.

## Technologies Covered

The uAgent can provide detailed educational content on:

- **Solana**: High-performance Layer 1 blockchain
- **SVM (Solana Virtual Machine)**: Runtime environment for Solana programs
- **SOON SVM**: Enhanced version of SVM for cross-chain interoperability
- **Walrus**: Decentralized storage protocol for blockchain applications
- **UTXO Model**: Transaction model used in Bitcoin and other chains
- **IBC Protocol**: Standardized protocol for cross-chain communication
- **ZPL UTXO Bridge**: Cross-chain solution for UTXO-based blockchains
- **WalletConnect Integration**: Wallet connectivity across multiple blockchains
- **Mainnet Deployment**: Production infrastructure for the Emrys platform

## Architecture

The uAgent system consists of three main components:

1. **model.py**: Contains the educational content database and formatting logic
2. **chat.py**: Implements the conversational interface using fetch.ai's chat protocol
3. **agent.py**: Defines the agent behavior, health checks, and protocol handlers

## Implementation Details

- Built on the fetch.ai uAgents framework
- Uses structured output for accurate protocol name detection
- Features a context-aware conversation system
- Provides multi-step reasoning for complex queries
- Includes domain-specific knowledge about blockchain technologies

## Usage

Users can interact with the uAgent through a chat interface to learn about any of the supported technologies. The uAgent will:

1. Parse the user's query to identify the requested technology
2. Retrieve detailed information about that technology
3. Format and return educational content in a structured, easy-to-read format
4. Suggest related technologies when queries are unclear

## Development

To set up the development environment:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the agent locally
python uagents/agent.py
```

## License

This project is part of the Emrys ecosystem. See the LICENSE file for details.

# Emrys uAgents

This directory contains uAgents for the Emrys platform.

## Agents

- **DeFi Protocol Information Agent**: Provides information about various blockchain technologies

## Railway Deployment

The agents can be deployed on Railway for easy hosting and scaling. 

For detailed instructions on deploying to Railway, see [RAILWAY.md](RAILWAY.md).

### Quick Start

1. Clone this repository
2. Navigate to the uagents directory
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the agent locally:
   ```
   python railway_agent.py
   ```
5. Test the agent:
   ```
   python test_agent.py
   ```

## Agent REST API

The Protocol Info Agent provides the following REST endpoints:

- **GET /health**: Health check endpoint
- **GET /protocols/list**: List all available protocols
- **POST /protocol/info**: Get information about a specific protocol

Example usage:
```bash
# Health check
curl http://localhost:8000/health

# List protocols
curl http://localhost:8000/protocols/list

# Get info about a protocol
curl -d '{"protocol_name": "solana"}' -H "Content-Type: application/json" -X POST http://localhost:8000/protocol/info
```

# Emrys - Cross-Chain Bridge and DeFi Platform

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)

This agent provides educational information about DeFi protocols and technologies within the Emrys ecosystem, focusing on the Solana ecosystem, SVM technologies, Cosmos IBC interoperability, and proprietary Emrys technologies. It uses fetch.ai uAgents technology to deliver comprehensive information about these specialized blockchain systems.

## Core Technologies

Emrys leverages several cutting-edge technologies to provide a seamless cross-chain experience:

### SOON SVM (Solana Virtual Machine)

A custom fork of the Solana Virtual Machine optimized for:
- High-throughput transaction processing (thousands of TPS)
- Parallel transaction execution for faster bridging operations
- Low-latency confirmations for reduced waiting times
- Robust smart contract execution for token locking and minting

### IBC (Inter-Blockchain Communication)

Backbone of Emrys' cross-chain functionality:
- Chain-agnostic messaging between heterogeneous blockchain networks
- Light client verification for cryptographic validation
- Trustless operation without central authorities
- Protocol-level security with cryptographic verification

### Walrus Decentralized Storage

Next-generation storage solution for:
- Immutable transaction records for all cross-chain operations
- Distributed data fragments across multiple nodes
- Rapid data retrieval from any chain
- Censorship resistance with no single point of failure
- Data encryption for privacy and security

### ZPL UTXO Bridge

Sophisticated cross-chain solution for:
- Connecting UTXO chains (Bitcoin, Dogecoin, Litecoin) with Solana
- Two-way peg mechanism for fully redeemable assets
- Hot/Cold reserve system for security
- Multi-cryptocurrency support with wrapped tokens

## Supported DeFi Protocols

The agent provides information across three main ecosystems:

### Solana Ecosystem
- **Solend**: Lending protocol on Solana
- **Orca**: DEX with concentrated liquidity
- **Raydium**: AMM integrated with Serum orderbook
- **Serum**: On-chain order book DEX
- **Marinade**: Liquid staking protocol
- **Jito**: MEV infrastructure and liquid staking
- **Jupiter**: Liquidity aggregator and routing
- **SVM**: Solana Virtual Machine technical details

### Cosmos Ecosystem
- **Osmosis**: IBC-enabled DEX
- **Astroport**: Multi-chain CosmWasm DEX
- **Mars Protocol**: Cross-chain lending
- **IBC**: Inter-Blockchain Communication protocol
- **Penumbra**: Private DeFi with zero-knowledge proofs

### Cross-Ecosystem
- **Pyth Network**: Oracle with Solana, EVM, and Cosmos support
- **Wormhole**: Cross-chain messaging between Solana, EVM chains, and Cosmos
- **ZPL UTXO Bridge**: Bridge between Bitcoin-like chains and Solana

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

### ZPL UTXO Bridge

The bridge enables secure transfer of assets between UTXO-based blockchains and Solana:
- Deposit BTC/DOGE/LTC and receive wrapped assets on Solana
- Two-way peg with fully redeemable assets
- Advanced security with hot/cold reserve systems
- Transaction history tracking via Walrus storage

## Installation and Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Run the agent:

```bash
python agent.py
```

## How It Works

1. **Natural Language Processing**: When a user asks a question about a protocol, the AI language model parses the query and extracts the relevant protocol name.

2. **Information Retrieval**: The agent looks up the protocol information in its specialized database and formats a comprehensive response.

3. **Response Generation**: The agent returns detailed information about the requested protocol, including:
   - Protocol name, category, and ecosystem
   - Description and launch date
   - Key features for users
   - Technical aspects focusing on SVM or IBC integration
   - Learning resources and documentation links

## Sample Interaction

User: "Tell me about SOON SVM"

Agent: *Returns detailed information about Emrys' custom SVM fork optimized for cross-chain operations, including its features and technical aspects.*

User: "How does the ZPL UTXO Bridge work?"

Agent: *Returns information about the ZPL UTXO Bridge, including its two-way peg mechanism, security model, and usage flows.*

## Technical Architecture

The agent consists of three main components:

1. **DeFi Protocol Module**: Contains the database of protocols and technologies, with detailed information about SOON SVM, IBC, Walrus, and the ZPL UTXO Bridge.

2. **Chat Protocol**: Handles the natural language communication with users and integrates with LLMs.

3. **Agent Core**: Manages the protocols, requests, rate limiting, and performs health checks across all technologies.

## Security Features

The information provided includes details on Emrys security features:
- Chain connection monitoring
- Transaction verification
- OFAC compliance checks
- Multi-stage approval process
- Audit trail via Walrus storage
- Hot/Cold reserve systems for UTXO bridges

## Extending the Agent

To add support for additional protocols or technologies, simply extend the `DEFI_PROTOCOLS` dictionary in `defi_protocol.py` with new entries following the same structure as existing protocols.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

***DISCLAIMER:*** *Emrys uses SVM & IBC & WALRUS for secure transactions & speed. All transactions are processed using our proprietary implementation of SVM (Solana Virtual Machine) and IBC (Inter-Blockchain Communication) protocols, with data secured through Walrus decentralized storage.*

## Agent Messaging

The Emrys DeFi Agent provides information through uAgent messaging:

### Protocol Information

To request protocol information, send a message to the agent with the following format:

```json
{
  "sender": "your-client-id",
  "destination": "emrys-defi-agent",
  "message": {
    "protocol_name": "SOON SVM" 
  }
}
```

Response:
```json
{
  "timestamp": 1234567890,
  "protocol_name": "SOON SVM",
  "information": "Detailed information about SOON SVM...",
  "agent_address": "agent1abc123..."
}
```

### Protocols List

For development purposes, the agent has a static list of supported protocols:
- SOON SVM
- IBC
- Walrus
- ZPL UTXO Bridge

## Development Setup

To run the agent locally:

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the agent:
   ```
   ./start.sh
   ```

The agent will start on port 8080 by default. You can override this by setting the `PORT` environment variable. 