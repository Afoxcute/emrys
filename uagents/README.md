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

# Emrys Solana & Cosmos DeFi Protocol Agent

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)

This agent provides educational information about DeFi protocols focused on the Solana ecosystem, SVM technologies, and Cosmos IBC interoperability. It uses fetch.ai uAgents technology to handle natural language queries and respond with structured information about these specialized blockchain ecosystems.

## Features

- Natural language interface using fetch.ai uAgents
- Comprehensive information on Solana and Cosmos DeFi protocols
- Detailed technical information about SVM (Solana Virtual Machine)
- In-depth explanations of IBC (Inter-Blockchain Communication) technology
- Integration with AI language models for query processing
- Modular design for easy extension with additional protocols
- Health monitoring system for reliability

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

User: "Tell me about Solend"

Agent: *Returns detailed information about Solend, including how it utilizes SVM for lending and borrowing on Solana.*

User: "How does Osmosis use IBC?"

Agent: *Returns information about Osmosis's IBC implementation, cross-chain liquidity, and interoperability with other Cosmos chains.*

## Technical Architecture

The agent consists of three main components:

1. **DeFi Protocol Module**: Contains the database of Solana and Cosmos protocols, with special attention to SVM and IBC integration details.

2. **Chat Protocol**: Handles the natural language communication with users and integrates with LLMs.

3. **Agent Core**: Manages the protocols, requests, rate limiting, and performs health checks across both ecosystems.

## Extending the Agent

To add support for additional protocols in the Solana or Cosmos ecosystems, simply extend the `DEFI_PROTOCOLS` dictionary in `defi_protocol.py` with new entries following the same structure as existing protocols.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 