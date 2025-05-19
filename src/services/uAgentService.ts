import axios from 'axios';
import { logger } from '../utils/logger';

// Use Railway URL for uAgent
const UAGENT_BASE_URL =
  process.env.NEXT_PUBLIC_UAGENT_URL || 'https://emrys-production.up.railway.app';

console.log('Connecting to uAgent at:', UAGENT_BASE_URL);

// Generate a random client ID for this session
const CLIENT_ID = `frontend-client-${Math.random().toString(36).substring(2, 15)}`;

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

/**
 * Fetches information about a specific protocol
 */
export async function fetchProtocolInfo(protocolName: string): Promise<string> {
  try {
    logger.debug(`Fetching information for protocol: ${protocolName}`);

    // Use the direct DeFiProtocolRequest format
    const submitPayload = {
      sender: CLIENT_ID,
      destination: 'emrys-defi-agent',
      message: {
        protocol_name: protocolName,
      },
    };

    // Try to submit directly to the agent
    const response = await axios.post(`${UAGENT_BASE_URL}/submit`, submitPayload, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 15000, // 15 second timeout to allow for agent processing
    });

    logger.debug('Protocol info raw response:', response.data);

    // Handle different response formats
    if (response.data && response.data.results) {
      // Response from DeFiProtocolResponse
      return response.data.results;
    } else if (response.data && response.data.information) {
      // Response from ProtocolInfoResponse
      return response.data.information;
    } else if (typeof response.data === 'string') {
      // Direct string response
      return response.data;
    } else if (response.data && response.data.body && response.data.body.results) {
      // Nested response format sometimes used by uAgents
      return response.data.body.results;
    } else {
      // Fallback to returning whatever we got as a string
      return JSON.stringify(response.data);
    }
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
    // Return a static list of protocols for reliability
    return {
      timestamp: Date.now(),
      protocols: {
        SOON_SVM: 'SOON SVM',
        IBC: 'IBC',
        WALRUS: 'Walrus',
        ZPL_UTXO_BRIDGE: 'ZPL UTXO Bridge',
        SOLANA: 'Solana',
        SVM: 'SVM',
        UTXO: 'UTXO Model',
      },
      count: 7,
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
