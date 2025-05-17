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