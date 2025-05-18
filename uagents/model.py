import requests
from uagents import Model, Field

class DeFiProtocolRequest(Model):
    protocol_name: str

class DeFiProtocolResponse(Model):
    results: str

# Dictionary of blockchain technologies with educational information
BLOCKCHAIN_TECHNOLOGIES = {
    "solana": {
        "name": "Solana",
        "category": "Layer 1 Blockchain",
        "launched": "2020",
        "description": "Solana is a high-performance blockchain supporting builders around the world creating crypto apps that scale. It features fast transaction speeds, low fees, and a growing ecosystem of applications spanning DeFi, NFTs, Web3, and more.",
        "key_features": [
            "Proof of History (PoH) consensus mechanism",
            "Up to 65,000 transactions per second (TPS)",
            "Sub-second block times",
            "Low transaction costs (average $0.00025 per transaction)",
            "Rich ecosystem of DeFi applications and NFT marketplaces"
        ],
        "technical_aspects": [
            "Uses Tower BFT consensus algorithm built on PoH",
            "8 key innovations including Turbine, Gulf Stream, Sealevel, Pipelining",
            "Account-based model unlike UTXO-based chains like Bitcoin",
            "Programs (smart contracts) written in Rust, C, C++, or any language that compiles to BPF"
        ],
        "learning_resources": [
            "https://docs.solana.com/",
            "https://solana.com/developers",
            "https://solana-labs.github.io/solana-web3.js/"
        ]
    },
    "svm": {
        "name": "SVM (Solana Virtual Machine)",
        "category": "Virtual Machine",
        "blockchain": "Solana",
        "description": "The Solana Virtual Machine (SVM) is the runtime environment in which Solana programs (smart contracts) execute. It uses the Berkeley Packet Filter (BPF) bytecode for deploying programs, which allows for efficient on-chain execution.",
        "key_features": [
            "Fast parallel transaction execution",
            "Support for multiple programming languages",
            "Low computational overhead",
            "Highly optimized for Solana's runtime environment",
            "Isolated program execution"
        ],
        "technical_aspects": [
            "Programs execute in BPF virtual machine",
            "Accounts store both code and data",
            "Uses Rust's memory safety and ownership model",
            "Supports parallel execution via Sealevel"
        ],
        "learning_resources": [
            "https://docs.solana.com/developing/on-chain-programs/overview",
            "https://docs.solana.com/developers",
            "https://github.com/solana-labs/solana-program-library"
        ]
    },
    "soon svm": {
        "name": "SOON SVM",
        "category": "Enhanced Solana Virtual Machine",
        "blockchain": "Solana Forks and Extensions",
        "description": "SOON SVM is an enhanced version of the Solana Virtual Machine designed specifically for cross-chain interoperability and high-throughput DeFi applications. It extends the standard SVM with additional capabilities for interchain communication and transaction processing.",
        "key_features": [
            "High-throughput transaction processing (thousands of TPS)",
            "Parallel transaction execution for faster bridging operations",
            "Low-latency confirmations reducing waiting times",
            "Robust smart contract execution for token locking and minting",
            "Cross-chain optimizations for efficient token transfers"
        ],
        "technical_aspects": [
            "Proprietary fork of the original Solana VM",
            "Enhanced security guarantees while maintaining speed",
            "Specialized for cross-chain operations",
            "Backward compatible with standard SVM programs",
            "Extended account model for interoperability"
        ],
        "learning_resources": [
            "https://github.com/solana-labs/solana (Base for understanding)",
            "Emrys documentation on SOON SVM implementation"
        ]
    },
    "walrus": {
        "name": "Walrus",
        "category": "Decentralized Storage",
        "application": "Cross-chain data verification and storage",
        "description": "Walrus is a decentralized storage protocol designed specifically for blockchain applications, focusing on immutability, data integrity, and high-performance access patterns. It provides a critical infrastructure layer for cross-chain applications requiring secure and verifiable data storage.",
        "key_features": [
            "Immutable transaction records for all cross-chain operations",
            "Distributed data fragments across multiple nodes",
            "Rapid data retrieval with low-latency access from any chain",
            "Censorship resistance with no single point of failure",
            "Data encryption before network storage"
        ],
        "technical_aspects": [
            "Uses erasure coding for data redundancy",
            "IPLD-compatible data format",
            "Merkle-based verification",
            "Incentivized storage providers",
            "On-chain anchoring of data commitments"
        ],
        "learning_resources": [
            "Emrys documentation on Walrus protocol",
            "GitHub repository for Walrus components"
        ]
    },
    "utxo": {
        "name": "UTXO Model",
        "category": "Blockchain Transaction Model",
        "used_in": "Bitcoin, Cardano, Dogecoin, Litecoin, ZPL",
        "description": "The Unspent Transaction Output (UTXO) model is a method of tracking ownership of cryptocurrency where each transaction consumes previous transaction outputs and creates new ones. Unlike account-based models (used in Ethereum and Solana), the UTXO model does not maintain account balances but tracks individual transaction outputs.",
        "key_features": [
            "Enhanced privacy as new addresses can be used for each transaction",
            "Naturally supports parallel transaction validation",
            "Simplifies payment verification (SPV)",
            "Prevents double-spending at the transaction level",
            "Stateless verification of transactions"
        ],
        "technical_aspects": [
            "Transactions consume inputs (previous UTXOs) and create outputs",
            "Each UTXO can only be spent once and in its entirety",
            "Change is returned as a new UTXO to the sender",
            "Requires script execution to validate spending conditions",
            "Enables complex spending conditions (time locks, multi-sig, etc.)"
        ],
        "learning_resources": [
            "https://bitcoin.org/en/developer-guide#transactions",
            "https://docs.cardano.org/plutus/eutxo-explainer",
            "Emrys documentation on ZPL UTXO implementation"
        ]
    },
    "zpl": {
        "name": "ZPL UTXO Bridge",
        "category": "Cross-Chain Bridge Protocol",
        "used_in": "Emrys Bridge between Bitcoin/Dogecoin/Litecoin and Solana",
        "description": "ZPL (UTXO Layer Protocol) is a sophisticated cross-chain solution that enables secure and efficient movement of assets between UTXO-based blockchains (like Bitcoin, Dogecoin, and Litecoin) and Solana's account-based system. It implements a two-way peg mechanism allowing users to deposit, withdraw, and manage assets across fundamentally different blockchain architectures.",
        "key_features": [
            "Cross-Chain Asset Movement: Deposit BTC/DOGE/LTC and receive wrapped assets (zBTC/zDOGE/zLTC) on Solana",
            "Two-Way Peg: Fully redeemable assets with bidirectional movement",
            "Hot/Cold Reserve System: Advanced security architecture for asset management",
            "Multi-Wallet Support: Integrates with various Bitcoin wallets",
            "Multi-Cryptocurrency Support: Works with Bitcoin, Dogecoin, and Litecoin",
            "Portfolio Management: Track and manage cross-chain assets",
            "Transaction History: View and track all cross-chain operations"
        ],
        "technical_aspects": [
            "UTXO Selection: Intelligent selection of UTXOs for optimal transaction fees",
            "Dust Management: Proper handling of dust amounts to prevent stuck funds",
            "Fee Estimation: Dynamic fee calculation based on network conditions",
            "P2TR Support: Native support for Pay-to-Taproot addresses",
            "Transaction Construction: Building, signing, and broadcasting transactions",
            "Hot Reserve: For regular deposit/withdrawal operations with time-locked scripts",
            "Cold Reserve: For secure long-term asset storage with recovery parameters",
            "Guardian System: Monitors and secures cross-chain operations",
            "Time-Locked Scripts: Provides security for user funds with specified unlock heights",
            "IBC Module: Handles inter-blockchain communication with light clients"
        ],
        "client_functions": [
            "Reserve Management: Managing hot and cold reserves for different cryptocurrencies",
            "Account Services: Creating and managing user accounts and positions",
            "Instruction Construction: Building Solana program instructions for all operations",
            "Transaction Signing: Handling transaction signing and submission",
            "Position Tracking: Monitoring user positions and balances"
        ],
        "usage_flows": {
            "deposit": [
                "Connect your Bitcoin and Solana wallets",
                "Select cryptocurrency type (BTC, DOGE, or LTC)",
                "Enter the amount to deposit",
                "Confirm the transaction in your wallet",
                "Once confirmed on the source chain, funds will be credited as wrapped tokens on Solana"
            ],
            "withdrawal": [
                "Connect your wallets",
                "Select cryptocurrency type",
                "Enter the amount to withdraw",
                "Choose a destination address",
                "Confirm the transaction with your Solana wallet",
                "Monitor the withdrawal status in the transaction history"
            ]
        },
        "learning_resources": [
            "Emrys documentation on ZPL UTXO Bridge",
            "https://docs.bitcoin.org/",
            "https://docs.solana.com/"
        ]
    },
    "ibc": {
        "name": "IBC (Inter-Blockchain Communication)",
        "category": "Cross-Chain Protocol",
        "used_in": "Cosmos Ecosystem, Emrys",
        "description": "The Inter-Blockchain Communication protocol (IBC) is a standardized protocol for secure communication between heterogeneous blockchains. It establishes a framework for transferring tokens and data across independent blockchain networks while maintaining the security properties of each chain.",
        "key_features": [
            "Chain-agnostic messaging: Standardized communication between heterogeneous blockchain networks",
            "Light client verification: Cryptographic validation of cross-chain messages",
            "Trustless operation: No central authority or validator set required for message relay",
            "Protocol-level security: Messages are cryptographically verified at the protocol level",
            "Permissionless connection establishment between chains"
        ],
        "technical_aspects": [
            "Two-layered architecture: Transport layer (TAO) and Application layer",
            "Connection handshake with light client verification",
            "Packet commitment for in-transit message verification",
            "Timeout mechanism for transaction safety",
            "Application-specific logic for packet handling"
        ],
        "learning_resources": [
            "https://ibcprotocol.org/",
            "https://github.com/cosmos/ibc",
            "https://tutorials.cosmos.network/academy/3-ibc/",
            "Emrys documentation on IBC implementation"
        ]
    },
    "zpl utxo bridge": {
        "name": "ZPL UTXO Bridge",
        "category": "Cross-Chain Bridge Protocol",
        "used_in": "Emrys Bridge between Bitcoin/Dogecoin/Litecoin and Solana",
        "description": "ZPL (UTXO Layer Protocol) is a sophisticated cross-chain solution that enables secure and efficient movement of assets between UTXO-based blockchains (like Bitcoin, Dogecoin, and Litecoin) and Solana's account-based system. It implements a two-way peg mechanism allowing users to deposit, withdraw, and manage assets across fundamentally different blockchain architectures.",
        "key_features": [
            "Cross-Chain Asset Movement: Deposit BTC/DOGE/LTC and receive wrapped assets (zBTC/zDOGE/zLTC) on Solana",
            "Two-Way Peg: Fully redeemable assets with bidirectional movement",
            "Hot/Cold Reserve System: Advanced security architecture for asset management",
            "Multi-Wallet Support: Integrates with various Bitcoin wallets",
            "Multi-Cryptocurrency Support: Works with Bitcoin, Dogecoin, and Litecoin",
            "Portfolio Management: Track and manage cross-chain assets",
            "Transaction History: View and track all cross-chain operations"
        ],
        "technical_aspects": [
            "UTXO Selection: Intelligent selection of UTXOs for optimal transaction fees",
            "Dust Management: Proper handling of dust amounts to prevent stuck funds",
            "Fee Estimation: Dynamic fee calculation based on network conditions",
            "P2TR Support: Native support for Pay-to-Taproot addresses",
            "Transaction Construction: Building, signing, and broadcasting transactions",
            "Hot Reserve: For regular deposit/withdrawal operations with time-locked scripts",
            "Cold Reserve: For secure long-term asset storage with recovery parameters",
            "Guardian System: Monitors and secures cross-chain operations",
            "Time-Locked Scripts: Provides security for user funds with specified unlock heights",
            "IBC Module: Handles inter-blockchain communication with light clients"
        ],
        "client_functions": [
            "Reserve Management: Managing hot and cold reserves for different cryptocurrencies",
            "Account Services: Creating and managing user accounts and positions",
            "Instruction Construction: Building Solana program instructions for all operations",
            "Transaction Signing: Handling transaction signing and submission",
            "Position Tracking: Monitoring user positions and balances"
        ],
        "usage_flows": {
            "deposit": [
                "Connect your Bitcoin and Solana wallets",
                "Select cryptocurrency type (BTC, DOGE, or LTC)",
                "Enter the amount to deposit",
                "Confirm the transaction in your wallet",
                "Once confirmed on the source chain, funds will be credited as wrapped tokens on Solana"
            ],
            "withdrawal": [
                "Connect your wallets",
                "Select cryptocurrency type",
                "Enter the amount to withdraw",
                "Choose a destination address",
                "Confirm the transaction with your Solana wallet",
                "Monitor the withdrawal status in the transaction history"
            ]
        },
        "learning_resources": [
            "Emrys documentation on ZPL UTXO Bridge",
            "https://docs.bitcoin.org/",
            "https://docs.solana.com/"
        ]
    },
    "walletconnect": {
        "name": "WalletConnect Integration",
        "category": "Wallet Connectivity Protocol",
        "used_in": "Emrys Bridge Interface",
        "description": "WalletConnect is an open protocol for connecting decentralized applications to mobile wallets with QR code scanning or deep linking. Emrys implements a comprehensive WalletConnect integration that provides a seamless wallet connection experience across multiple blockchain ecosystems.",
        "key_features": [
            "Multi-protocol support: Connect wallets across EVM, Cosmos, Solana, and Starknet ecosystems",
            "Wide wallet compatibility: Support for dozens of popular wallets across different blockchains",
            "Mobile and desktop compatibility: Consistent connection experience across devices",
            "QR code and deep linking: Easy connection methods for mobile users",
            "Session management: Persistent connections with customizable timeouts",
            "Chain switching: Seamless switching between supported blockchains"
        ],
        "wallet_compatibility": {
            "EVM chains": [
                "MetaMask",
                "Coinbase Wallet",
                "Rainbow",
                "Trust Wallet", 
                "Ledger"
            ],
            "Cosmos chains": [
                "Keplr",
                "Cosmostation",
                "Leap"
            ],
            "Solana": [
                "Phantom",
                "Solflare",
                "Snap Wallet",
                "Trust Wallet"
            ],
            "Starknet": [
                "Supported via StarknetConfig"
            ]
        },
        "technical_aspects": [
            "WalletConnect v2 Protocol integration",
            "Multi-chain signing capability",
            "Easy-to-use connector API",
            "End-to-end encryption",
            "Responsive QR code generation",
            "Chain namespace handling",
            "Error recovery mechanisms"
        ],
        "implementation_details": [
            "React hooks for wallet state management",
            "Multi-provider architecture",
            "Chain-specific connection handling",
            "Metadata customization for clear wallet identification",
            "Automatic network detection and switching"
        ],
        "learning_resources": [
            "https://docs.walletconnect.com/",
            "Emrys documentation on wallet integration",
            "https://github.com/WalletConnect/walletconnect-monorepo"
        ]
    },
    "mainnet": {
        "name": "Mainnet Deployment",
        "category": "Production Infrastructure",
        "used_in": "Emrys Bridge Production Environment",
        "description": "Emrys is designed with production-ready infrastructure for secure, reliable, and performant mainnet deployment. The platform incorporates numerous features that ensure stability, security, and compliance when handling real assets across multiple blockchains.",
        "key_features": [
            "Production chain configurations: Pre-configured mainnet settings for Solana, Eclipse, EVMOS, and more",
            "Verified contract addresses: Integration with Hyperlane registry for secure contract interactions",
            "Sanction compliance: Real-time checking against Chainalysis and OFAC sanctions lists",
            "Gas optimization: Production-calibrated gas settings for each supported chain",
            "Analytics and monitoring: Production metrics through Vercel Analytics",
            "Security headers: Advanced security configurations for production environments",
            "Dynamic RPC fallbacks: Automatic fallback to alternate RPC endpoints for maximum reliability",
            "Cross-chain messaging security: Production-grade verification for all cross-chain messages"
        ],
        "architecture_components": [
            "Frontend: Next.js with TypeScript and TailwindCSS",
            "Smart Contracts: Solana programs and EVM contracts",
            "Monitoring: Real-time transaction tracking and error reporting",
            "Security: Multi-layered protection with compliance checks",
            "Bridge Infrastructure: SOON SVM for execution",
            "Data Storage: Walrus for transaction records",
            "Cross-chain Communication: IBC protocol implementation"
        ],
        "security_features": [
            "Chain connection monitoring: Active verification of chain health",
            "Transaction verification: Multi-step validation of cross-chain transactions",
            "OFAC compliance checks: Real-time screening against sanctions lists",
            "Multi-stage approval process: Required for high-value transactions",
            "Audit trail: Comprehensive transaction history via Walrus storage"
        ],
        "technical_aspects": [
            "CI/CD pipeline for reliable deployments",
            "Robust error handling for transaction edge cases",
            "Caching strategies for optimal performance",
            "Redundant infrastructure for high availability",
            "Rate limiting to prevent abuse"
        ],
        "learning_resources": [
            "Emrys documentation on production deployment",
            "https://docs.solana.com/running-validator",
            "https://docs.hyperlane.xyz/"
        ]
    }
}

async def get_protocol_info(protocol_name: str) -> str:
    """
    Fetch blockchain technology information from our database and return as plain text
    """
    try:
        # Convert to lowercase for case-insensitive matching
        protocol_key = protocol_name.lower()
        
        # Check if the technology exists in our database
        if protocol_key in BLOCKCHAIN_TECHNOLOGIES:
            technology = BLOCKCHAIN_TECHNOLOGIES[protocol_key]
            
            # Format the technology information as a structured text
            result = f"\n{technology['name']} - {technology['category']}\n"
            
            # Add blockchain/used_in/application info if available
            if 'blockchain' in technology:
                result += f"Blockchain: {technology['blockchain']}\n"
            if 'used_in' in technology:
                result += f"Used in: {technology['used_in']}\n"
            if 'launched' in technology:
                result += f"Launched: {technology['launched']}\n"
            if 'application' in technology:
                result += f"Application: {technology['application']}\n"
            
            result += f"\nDescription:\n{technology['description']}\n\n"
            
            result += "Key Features:\n"
            for feature in technology['key_features']:
                result += f"- {feature}\n"
            
            # Add wallet compatibility if available
            if 'wallet_compatibility' in technology:
                result += "\nWallet Compatibility:\n"
                for chain, wallets in technology['wallet_compatibility'].items():
                    result += f"{chain}:\n"
                    for wallet in wallets:
                        result += f"- {wallet}\n"
                    result += "\n"
            
            # Add architecture components if available
            if 'architecture_components' in technology:
                result += "\nArchitecture Components:\n"
                for component in technology['architecture_components']:
                    result += f"- {component}\n"
            
            # Add security features if available  
            if 'security_features' in technology:
                result += "\nSecurity Features:\n"
                for feature in technology['security_features']:
                    result += f"- {feature}\n"
                    
            # Add implementation details if available
            if 'implementation_details' in technology:
                result += "\nImplementation Details:\n"
                for detail in technology['implementation_details']:
                    result += f"- {detail}\n"
            
            # Add technical aspects
            result += "\nTechnical Aspects:\n"
            for aspect in technology['technical_aspects']:
                result += f"- {aspect}\n"
            
            # Add client functions if available
            if 'client_functions' in technology:
                result += "\nClient Functions:\n"
                for function in technology['client_functions']:
                    result += f"- {function}\n"
            
            # Add usage flows if available
            if 'usage_flows' in technology:
                result += "\nUsage Flows:\n"
                for flow_name, steps in technology['usage_flows'].items():
                    result += f"\n{flow_name.capitalize()} Flow:\n"
                    for i, step in enumerate(steps, 1):
                        result += f"{i}. {step}\n"
            
            result += "\nLearning Resources:\n"
            for resource in technology['learning_resources']:
                result += f"- {resource}\n"
            
            return result
        else:
            # Similar technologies suggestion
            similar_technologies = []
            search_term = protocol_key.lower()
            
            # List of all technologies we support
            all_technologies = ["solana", "svm", "soon svm", "walrus", "utxo", "ibc", "zpl", "zpl utxo bridge", "walletconnect", "mainnet"]
            
            # Check for partial matches
            for key in all_technologies:
                if search_term in key or key in search_term:
                    similar_technologies.append(BLOCKCHAIN_TECHNOLOGIES.get(key, {}).get('name', key.upper()))
            
            # If no matches found by key, try searching in descriptions
            if not similar_technologies:
                for key, tech in BLOCKCHAIN_TECHNOLOGIES.items():
                    if search_term in tech['description'].lower():
                        similar_technologies.append(tech['name'])
            
            if similar_technologies:
                suggestions = ", ".join(similar_technologies)
                return f"'{protocol_name}' not found. Did you mean one of these: {suggestions}?"
            else:
                return f"Information about '{protocol_name}' not found in our database. Please try one of these technologies: Solana, SVM, Soon SVM, Walrus, UTXO, IBC, ZPL UTXO Bridge, WalletConnect Integration, or Mainnet Deployment."
            
    except Exception as e:
        return f"Error fetching technology information: {str(e)}"