/* eslint-disable no-console */
import axios from 'axios';
import { logger } from '../utils/logger';

// Use Railway URL for uAgent without appending the port in the URL
// The PORT is already configured in the agent and handled by Railway
let UAGENT_BASE_URL =
  process.env.NEXT_PUBLIC_UAGENT_URL || 'https://emrys-production.up.railway.app';

// Remove any port number if present in the URL
if (UAGENT_BASE_URL.includes(':8080')) {
  UAGENT_BASE_URL = UAGENT_BASE_URL.replace(':8080', '');
}

// Log connection info
logger.info('Connecting to uAgent at:', UAGENT_BASE_URL);

export interface ProtocolInfo {
  timestamp: number;
  protocolName: string;
  information: string;
  agent_address: string;
}

export interface ProtocolsListResponse {
  timestamp: number;
  protocols: Record<string, string>;
  count: number;
}

// Static protocol info for common queries to avoid timeouts
const STATIC_PROTOCOL_INFO: Record<string, string> = {
  'soon svm': `SOON SVM (Solana Virtual Machine) is a custom fork of the Solana Virtual Machine optimized for cross-chain operations. Key features include high-throughput transaction processing (thousands of TPS), parallel transaction execution for faster bridging operations, low-latency confirmations for reduced waiting times, and robust smart contract execution for token locking and minting. It forms the execution layer of the Emrys bridge platform.`,

  ibc: `IBC (Inter-Blockchain Communication) is the backbone of Emrys' cross-chain functionality. It provides chain-agnostic messaging between heterogeneous blockchain networks, light client verification for cryptographic validation, trustless operation without central authorities, and protocol-level security with cryptographic verification. IBC enables seamless asset transfer between Cosmos and Solana ecosystems.`,

  walrus: `Walrus is a next-generation decentralized storage solution for blockchain applications. It provides immutable transaction records for all cross-chain operations, distributes data fragments across multiple nodes, enables rapid data retrieval from any chain, offers censorship resistance with no single point of failure, and implements data encryption for privacy and security. Walrus is integral to Emrys' cross-chain infrastructure.`,

  zpl: `The ZPL UTXO Bridge is a sophisticated cross-chain solution that connects UTXO chains (Bitcoin, Dogecoin, Litecoin) with Solana. It implements a two-way peg mechanism for fully redeemable assets, employs a hot/cold reserve system for enhanced security, and supports multiple cryptocurrencies with wrapped tokens. The bridge enables secure and efficient transfers between Bitcoin-like blockchains and the Solana ecosystem.`,

  solana: `Solana is a high-performance Layer 1 blockchain known for its remarkable speed and low transaction costs. It uses a unique Proof of History consensus mechanism combined with Proof of Stake, allowing for parallel transaction processing and theoretical throughput of over 65,000 transactions per second. The Emrys platform leverages Solana's capabilities to provide fast and efficient cross-chain operations.`,
};

/**
 * Fetches information about a specific protocol
 */
export async function fetchProtocolInfo(protocolName: string): Promise<string> {
  try {
    // First check if we have static info for this protocol
    const normalizedName = protocolName.toLowerCase().trim();

    // Check for exact matches or partial matches in static data
    for (const [key, value] of Object.entries(STATIC_PROTOCOL_INFO)) {
      if (key === normalizedName || normalizedName.includes(key) || key.includes(normalizedName)) {
        logger.debug(`Using static protocol info for "${normalizedName}"`);
        return value;
      }
    }

    // Fallback to generic info if no match found
    return `Information about ${protocolName} is currently being updated. The Emrys platform supports various technologies including SOON SVM, IBC for cross-chain communication, Walrus for decentralized storage, and ZPL UTXO Bridge for connecting Bitcoin-like chains to Solana. Please ask about one of these specific technologies for more details.`;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      logger.error(`Error fetching protocol info for ${protocolName}:`, error.response.data);
      throw new Error(`No information found for ${protocolName}`);
    } else {
      logger.error(`Error fetching protocol info for ${protocolName}:`, error);
      throw new Error('Failed to connect to protocol information service');
    }
  }
}

/**
 * Fetches the list of all available protocols
 */
export async function fetchProtocolsList(): Promise<ProtocolsListResponse> {
  try {
    // Return static list of protocols to avoid timeouts
    return {
      timestamp: Date.now(),
      protocols: {
        SOON_SVM: 'SOON SVM',
        IBC: 'IBC',
        WALRUS: 'Walrus',
        ZPL: 'ZPL UTXO Bridge',
        SOLANA: 'Solana',
      },
      count: 5,
    };
  } catch (error) {
    logger.error('Error fetching protocols list:', error);
    throw new Error('Failed to fetch available protocols');
  }
}

/**
 * Checks if the uAgent service is healthy
 * Always returns true because we're removing the health check functionality
 */
export async function checkUAgentHealth(): Promise<boolean> {
  // Assume the agent is always available
  return true;
}
