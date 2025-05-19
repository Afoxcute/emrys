import requests
from uagents import Model

class DeFiProtocolRequest(Model):
    protocol_name: str

class DeFiProtocolResponse(Model):
    results: str

# Dictionary of DeFi protocols with educational information focused on Solana, SVM, and Cosmos IBC
DEFI_PROTOCOLS = {
    "solend": {
        "name": "Solend",
        "category": "Lending Protocol",
        "launched": "2021",
        "blockchain": "Solana",
        "ecosystem": "Solana",
        "description": "Solend is an algorithmic, decentralized protocol for lending and borrowing on Solana. As Solana's first lending protocol, it enables users to earn interest on deposits and borrow assets against collateral while taking advantage of Solana's high speeds and low fees.",
        "key_features": [
            "High-speed lending and borrowing on Solana",
            "Low transaction fees (<$0.01 per transaction)",
            "Multiple supported assets including SOL, USDC, and BTC",
            "Governance through SLND token",
            "Variable interest rates based on utilization",
            "Instant transaction finality"
        ],
        "technical_aspects": [
            "Built on Solana Program Library (SPL) token standard",
            "SLP tokens represent deposit positions",
            "Serum DEX integration for liquidations",
            "Risk parameters set by governance",
            "Pyth oracle network for accurate price feeds",
            "SVM (Solana Virtual Machine) program execution"
        ],
        "learning_resources": [
            "https://solend.fi/",
            "https://docs.solend.fi/",
            "https://github.com/solendprotocol"
        ]
    },
    "orca": {
        "name": "Orca",
        "category": "Decentralized Exchange (DEX)",
        "launched": "2021",
        "blockchain": "Solana",
        "ecosystem": "Solana",
        "description": "Orca is a user-friendly decentralized exchange built on Solana that focuses on simplicity and the best prices for traders through its concentrated liquidity and Whirlpools features. It's designed to provide a seamless trading experience with minimal fees and maximum capital efficiency.",
        "key_features": [
            "Concentrated liquidity pools (Whirlpools)",
            "Fair price execution",
            "Simple, intuitive interface",
            "Low transaction costs",
            "Liquidity provider incentives through ORCA token",
            "Fair Launch tokenomics"
        ],
        "technical_aspects": [
            "SVM-based smart contracts for trading logic",
            "Constant product AMM for standard pools",
            "Concentrated liquidity implementation for Whirlpools",
            "Price impact protection",
            "Composable DeFi primitives",
            "On-chain price oracles"
        ],
        "learning_resources": [
            "https://www.orca.so/",
            "https://docs.orca.so/",
            "https://github.com/orca-so"
        ]
    },
    "raydium": {
        "name": "Raydium",
        "category": "Automated Market Maker (AMM)",
        "launched": "2021",
        "blockchain": "Solana",
        "ecosystem": "Solana",
        "description": "Raydium is an automated market maker (AMM) built on Solana that provides on-chain liquidity to a central limit order book, enabling lightning-fast trades, shared liquidity, and the ability to place limit orders. It powers the Raydium ecosystem with farms, staking, and liquidity pools.",
        "key_features": [
            "Hybrid AMM integrated with Serum order book",
            "Sub-second transaction finality",
            "Low-cost swaps and trades",
            "AcceleRaytor launchpad for new projects",
            "Fusion pools for concentrated farming",
            "RAY token governance and incentives"
        ],
        "technical_aspects": [
            "SVM program architecture",
            "Shared liquidity between AMM and order book",
            "SPL token standard integration",
            "Price curves optimized for efficient trading",
            "Permissionless liquidity provision",
            "Smart-routing for best execution price"
        ],
        "learning_resources": [
            "https://raydium.io/",
            "https://docs.raydium.io/",
            "https://github.com/raydium-io"
        ]
    },
    "serum": {
        "name": "Serum",
        "category": "Decentralized Exchange (DEX)",
        "launched": "2020",
        "blockchain": "Solana",
        "ecosystem": "Solana",
        "description": "Serum is a decentralized exchange protocol built on Solana that brings the speed and efficiency of central limit order books to DeFi. It serves as infrastructure for the entire Solana DeFi ecosystem, enabling composable trading, lending, and borrowing through its on-chain order book.",
        "key_features": [
            "On-chain central limit order book (CLOB)",
            "Cross-chain trading capabilities",
            "Microsecond transaction times",
            "Composable DeFi infrastructure",
            "Low transaction fees",
            "SRM token for fee discounts and governance"
        ],
        "technical_aspects": [
            "Full on-chain order book with price-time priority",
            "SVM execution environment for transaction processing",
            "Permissionless market creation",
            "Atomic settlement of trades",
            "Cross-program invocation (CPI) for composability",
            "SPL token integration"
        ],
        "learning_resources": [
            "https://www.projectserum.com/",
            "https://docs.projectserum.com/",
            "https://github.com/project-serum"
        ]
    },
    "marinade": {
        "name": "Marinade Finance",
        "category": "Liquid Staking",
        "launched": "2021",
        "blockchain": "Solana",
        "ecosystem": "Solana",
        "description": "Marinade Finance is a non-custodial liquid staking protocol built on Solana that allows users to stake SOL and receive mSOL, a liquid staking token that can be used across the Solana DeFi ecosystem while still earning staking rewards. It's designed to increase the capital efficiency of staked assets.",
        "key_features": [
            "Liquid staking solution for SOL",
            "mSOL token that automatically compounds rewards",
            "Integration with Solana DeFi applications",
            "Decentralized validator set",
            "MNDE governance token",
            "Stake distribution algorithm for network health"
        ],
        "technical_aspects": [
            "Validator selection algorithm for decentralization",
            "SVM programs for stake management",
            "Epoch-based reward distribution",
            "Delayed unstaking mechanism for security",
            "State modeling for efficient processing",
            "Liquid staking token (mSOL) implementation"
        ],
        "learning_resources": [
            "https://marinade.finance/",
            "https://docs.marinade.finance/",
            "https://github.com/marinade-finance"
        ]
    },
    "jito": {
        "name": "Jito",
        "category": "MEV Infrastructure",
        "launched": "2022",
        "blockchain": "Solana",
        "ecosystem": "Solana",
        "description": "Jito is a MEV (Maximal Extractable Value) infrastructure for Solana that provides a suite of tools including a block engine, MEV searcher, and liquid staking protocol. It allows for more efficient block space usage and fairer transaction ordering while letting users earn additional rewards through JitoSOL liquid staking.",
        "key_features": [
            "MEV-aware validator client",
            "JitoSOL liquid staking token",
            "MEV searcher network",
            "Tip distribution mechanism",
            "Validator block space auction",
            "Enhanced network performance"
        ],
        "technical_aspects": [
            "SVM-optimized transactions for MEV extraction",
            "Custom block building algorithm",
            "Tip account infrastructure",
            "ProgramID prioritization mechanism",
            "Liquid staking implementation",
            "Custom Solana validator client"
        ],
        "learning_resources": [
            "https://jito.network/",
            "https://docs.jito.network/",
            "https://github.com/jito-foundation"
        ]
    },
    "jupiter": {
        "name": "Jupiter",
        "category": "Aggregator",
        "launched": "2021",
        "blockchain": "Solana",
        "ecosystem": "Solana",
        "description": "Jupiter is the key liquidity aggregator for Solana, providing the best swap routes across all Solana DEXes. It analyzes dozens of liquidity sources to ensure users get the best prices for their swaps, with advanced routing algorithms and split trades to minimize slippage and maximize capital efficiency.",
        "key_features": [
            "Smart routing across multiple DEXes",
            "Price impact protection",
            "Split routes for large trades",
            "Minimal fees",
            "High-performance infrastructure",
            "Jupiter Terminal for all-in-one trading"
        ],
        "technical_aspects": [
            "Multi-route pathfinding algorithm",
            "On-chain swap execution via SVM",
            "Composable swap infrastructure",
            "Transaction simulation for safety",
            "Versioned transactions support",
            "Real-time price updates"
        ],
        "learning_resources": [
            "https://jup.ag/",
            "https://docs.jup.ag/",
            "https://github.com/jup-ag"
        ]
    },
    "svm": {
        "name": "Solana Virtual Machine (SVM)",
        "category": "Blockchain Runtime",
        "launched": "2020",
        "blockchain": "Solana",
        "ecosystem": "Solana",
        "description": "The Solana Virtual Machine (SVM) is the runtime environment in which Solana smart contracts, called programs, execute. It uses the Berkeley Packet Filter (BPF) bytecode for deploying programs, which enables parallel transaction processing and high-throughput execution that powers Solana's DeFi ecosystem.",
        "key_features": [
            "Parallel transaction execution",
            "Support for multiple languages (Rust, C, C++)",
            "Low computational overhead",
            "Predictable gas costs",
            "Account-based architecture",
            "High-performance execution"
        ],
        "technical_aspects": [
            "BPF (Berkeley Packet Filter) bytecode compilation",
            "Sealevel parallel runtime",
            "Account model for state management",
            "Cross-Program Invocation (CPI) for composability",
            "Program Derived Addresses (PDAs)",
            "Rent economics for state storage"
        ],
        "learning_resources": [
            "https://docs.solana.com/developing/on-chain-programs/overview",
            "https://solanacookbook.com/",
            "https://github.com/solana-labs/solana-program-library"
        ]
    },
    "osmosis": {
        "name": "Osmosis",
        "category": "Decentralized Exchange (DEX)",
        "launched": "2021",
        "blockchain": "Cosmos",
        "ecosystem": "Cosmos",
        "description": "Osmosis is a decentralized, cross-chain automated market maker (AMM) protocol built on the Cosmos SDK, leveraging IBC (Inter-Blockchain Communication) protocol to enable seamless cross-chain trading. It allows users to create liquidity pools, trade tokens from different blockchains, and participate in governance.",
        "key_features": [
            "IBC-enabled cross-chain trading",
            "Custom pool types with adjustable parameters",
            "On-chain governance through OSMO token",
            "Superfluid staking",
            "Interchain accounts",
            "Incentivized liquidity pools"
        ],
        "technical_aspects": [
            "Cosmos SDK for blockchain infrastructure",
            "IBC protocol for cross-chain communication",
            "Multiple AMM curve types",
            "CosmWasm for smart contract functionality",
            "Tendermint consensus algorithm",
            "Interchain security model"
        ],
        "learning_resources": [
            "https://osmosis.zone/",
            "https://docs.osmosis.zone/",
            "https://github.com/osmosis-labs"
        ]
    },
    "astroport": {
        "name": "Astroport",
        "category": "Decentralized Exchange (DEX)",
        "launched": "2021",
        "blockchain": "Terra, Injective, Neutron",
        "ecosystem": "Cosmos",
        "description": "Astroport is a neutral marketplace where anyone can create liquidity pools, swap assets from different blockchains, and participate in governance. It's built using CosmWasm smart contracts and leverages IBC for interoperability across the Cosmos ecosystem, supporting multiple pool types for optimal trading.",
        "key_features": [
            "Multi-chain deployment across Cosmos zones",
            "IBC token support for cross-chain liquidity",
            "Multiple pool types (constant product, stable, concentrated)",
            "Governance via ASTRO token",
            "Fee-sharing with stakers",
            "Protocol-owned liquidity"
        ],
        "technical_aspects": [
            "CosmWasm smart contracts",
            "IBC protocol integration",
            "Cross-chain transaction routing",
            "Multiple pricing curves for different asset types",
            "Tokenomics design supporting multi-chain growth",
            "Governance-controlled parameters"
        ],
        "learning_resources": [
            "https://astroport.fi/",
            "https://docs.astroport.fi/",
            "https://github.com/astroport-fi"
        ]
    },
    "mars": {
        "name": "Mars Protocol",
        "category": "Lending Protocol",
        "launched": "2022",
        "blockchain": "Terra, Osmosis, Neutron",
        "ecosystem": "Cosmos",
        "description": "Mars Protocol is a credit protocol built using CosmWasm smart contracts that enables non-custodial borrowing and lending across multiple Cosmos chains. It leverages IBC for cross-chain functionality, allowing users to deposit assets on one chain and borrow assets on another chain within the Cosmos ecosystem.",
        "key_features": [
            "Cross-chain borrowing and lending via IBC",
            "Isolated lending markets for risk management",
            "Leveraged yield farming",
            "MARS token governance",
            "Red Bank for permissionless lending",
            "Credit accounts for advanced strategies"
        ],
        "technical_aspects": [
            "CosmWasm smart contracts",
            "IBC protocol for cross-chain asset transfers",
            "Risk-adjusted interest rate model",
            "Liquidity mining incentives",
            "Isolated collateral markets",
            "Governance-controlled risk parameters"
        ],
        "learning_resources": [
            "https://marsprotocol.io/",
            "https://docs.marsprotocol.io/",
            "https://github.com/mars-protocol"
        ]
    },
    "ibc": {
        "name": "Inter-Blockchain Communication (IBC)",
        "category": "Cross-Chain Protocol",
        "launched": "2021",
        "blockchain": "Cosmos Ecosystem",
        "ecosystem": "Cosmos",
        "description": "IBC (Inter-Blockchain Communication) is a protocol for secure communication between heterogeneous blockchains, primarily used in the Cosmos ecosystem but extendable to other blockchains. It enables cross-chain token transfers, interchain accounts, and cross-chain smart contract calls, making it the backbone of interoperability in Cosmos.",
        "key_features": [
            "Trustless cross-chain communication",
            "Transfer of tokens between chains",
            "Interchain accounts (ICAs)",
            "Cross-chain smart contract calls",
            "Light client verification",
            "Packet relay system"
        ],
        "technical_aspects": [
            "Light client verification for security",
            "Connection, channel, and port abstractions",
            "Packet commitment and verification",
            "Ordered and unordered channels",
            "Timeout handling for liveness",
            "Relayer infrastructure for message passing"
        ],
        "learning_resources": [
            "https://ibcprotocol.org/",
            "https://tutorials.cosmos.network/academy/3-ibc/",
            "https://github.com/cosmos/ibc"
        ]
    },
    "penumbra": {
        "name": "Penumbra",
        "category": "Private DeFi",
        "launched": "2023",
        "blockchain": "Penumbra Zone",
        "ecosystem": "Cosmos",
        "description": "Penumbra is a private DeFi protocol built on the Cosmos SDK that uses zero-knowledge proofs to provide privacy for transactions, swaps, and staking. It leverages IBC to enable private cross-chain transactions, allowing users to interact with the broader Cosmos ecosystem while maintaining privacy.",
        "key_features": [
            "Private token transfers and swaps",
            "Zero-knowledge proof technology",
            "IBC-enabled cross-chain privacy",
            "Private AMM for decentralized trading",
            "Shielded staking",
            "Multi-asset support"
        ],
        "technical_aspects": [
            "zk-SNARKs for transaction privacy",
            "IBC protocol integration",
            "Custom consensus mechanism",
            "Decentralized note system",
            "Multi-asset shielded pool",
            "ZSwap private AMM implementation"
        ],
        "learning_resources": [
            "https://penumbra.zone/",
            "https://guide.penumbra.zone/",
            "https://github.com/penumbra-zone"
        ]
    },
    "pyth": {
        "name": "Pyth Network",
        "category": "Oracle",
        "launched": "2021",
        "blockchain": "Solana, Ethereum, Cosmos",
        "ecosystem": "Cross-Ecosystem",
        "description": "Pyth Network is a first-party oracle that publishes financial market data directly on-chain for use by DeFi applications. It provides high-fidelity, low-latency price feeds for cryptocurrencies, equities, FX pairs, and commodities, using a unique confidence interval approach. Pyth operates across multiple ecosystems including Solana, Ethereum, and Cosmos via IBC.",
        "key_features": [
            "High-frequency price updates (~400ms)",
            "First-party data from major trading firms",
            "Cross-chain availability (Solana, EVM, Cosmos)",
            "Price confidence intervals",
            "Push oracle design",
            "Permissionless publisher verification"
        ],
        "technical_aspects": [
            "On-chain price aggregation",
            "Wormhole cross-chain messaging",
            "IBC protocol integration for Cosmos chains",
            "SVM-based on-chain programs",
            "TWAP support for DeFi integrations",
            "Publisher stake-weighted aggregation"
        ],
        "learning_resources": [
            "https://pyth.network/",
            "https://docs.pyth.network/",
            "https://github.com/pyth-network"
        ]
    },
    "wormhole": {
        "name": "Wormhole",
        "category": "Cross-Chain Messaging",
        "launched": "2021",
        "blockchain": "Solana, Ethereum, Cosmos",
        "ecosystem": "Cross-Ecosystem",
        "description": "Wormhole is a generic cross-chain messaging protocol that enables communication between Solana, Ethereum, Cosmos, and other major blockchains. It allows for token transfers, NFT movements, and arbitrary message passing between chains, connecting siloed blockchain ecosystems through a unified messaging layer.",
        "key_features": [
            "Generic message passing between chains",
            "Cross-chain token bridge",
            "NFT bridge functionality",
            "Support for 20+ blockchains",
            "Guardian network for security",
            "Composable cross-chain applications"
        ],
        "technical_aspects": [
            "SVM core contracts on Solana",
            "IBC-compatible for Cosmos integration",
            "Threshold signature scheme for security",
            "VAA (Verifiable Action Approval) system",
            "Consistent addressing across chains",
            "Upgradable on-chain contracts"
        ],
        "learning_resources": [
            "https://wormhole.com/",
            "https://docs.wormhole.com/",
            "https://github.com/wormhole-foundation"
        ]
    }
}

async def get_defi_protocol_info(protocol_name: str) -> str:
    """
    Fetch DeFi protocol information from our database and return as plain text
    """
    try:
        # Convert to lowercase for case-insensitive matching
        protocol_key = protocol_name.lower()
        
        # Check if the protocol exists in our database
        if protocol_key in DEFI_PROTOCOLS:
            protocol = DEFI_PROTOCOLS[protocol_key]
            
            # Format the protocol information as a structured text
            result = f"\n{protocol['name']} - {protocol['category']}\n"
            
            # Add blockchain/ecosystem/launched info if available
            if 'blockchain' in protocol:
                result += f"Blockchain: {protocol['blockchain']}\n"
            if 'ecosystem' in protocol:
                result += f"Ecosystem: {protocol['ecosystem']}\n"
            if 'launched' in protocol:
                result += f"Launched: {protocol['launched']}\n"
            
            result += f"\nDescription:\n{protocol['description']}\n\n"
            
            result += "Key Features:\n"
            for feature in protocol['key_features']:
                result += f"- {feature}\n"
            
            result += "\nTechnical Aspects:\n"
            for aspect in protocol['technical_aspects']:
                result += f"- {aspect}\n"
            
            result += "\nLearning Resources:\n"
            for resource in protocol['learning_resources']:
                result += f"- {resource}\n"
            
            return result
        else:
            # Similar protocols suggestion
            similar_protocols = []
            search_term = protocol_key.lower()
            
            # List of all protocols we support
            all_protocols = list(DEFI_PROTOCOLS.keys())
            
            # Check for partial matches
            for key in all_protocols:
                if search_term in key or key in search_term:
                    similar_protocols.append(DEFI_PROTOCOLS.get(key, {}).get('name', key.upper()))
            
            # If no matches found by key, try searching in descriptions
            if not similar_protocols:
                for key, proto in DEFI_PROTOCOLS.items():
                    if search_term in proto['description'].lower():
                        similar_protocols.append(proto['name'])
            
            if similar_protocols:
                suggestions = ", ".join(similar_protocols)
                return f"'{protocol_name}' not found. Did you mean one of these: {suggestions}?"
            else:
                solana_protocols = [DEFI_PROTOCOLS[k]["name"] for k in DEFI_PROTOCOLS if DEFI_PROTOCOLS[k].get("ecosystem") == "Solana"]
                cosmos_protocols = [DEFI_PROTOCOLS[k]["name"] for k in DEFI_PROTOCOLS if DEFI_PROTOCOLS[k].get("ecosystem") == "Cosmos"]
                cross_protocols = [DEFI_PROTOCOLS[k]["name"] for k in DEFI_PROTOCOLS if DEFI_PROTOCOLS[k].get("ecosystem") == "Cross-Ecosystem"]
                
                result = f"Information about '{protocol_name}' not found in our database. Please try one of these protocols:\n\n"
                
                result += "Solana Ecosystem: " + ", ".join(solana_protocols) + "\n\n"
                result += "Cosmos Ecosystem: " + ", ".join(cosmos_protocols) + "\n\n"
                result += "Cross-Ecosystem: " + ", ".join(cross_protocols)
                
                return result
            
    except Exception as e:
        return f"Error fetching DeFi protocol information: {str(e)}" 