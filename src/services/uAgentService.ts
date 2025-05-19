import axios from 'axios';
import { logger } from '../utils/logger';

// Use Railway URL for uAgent
const UAGENT_BASE_URL =
  process.env.NEXT_PUBLIC_UAGENT_URL || 'https://emrys-production.up.railway.app';

console.log('Connecting to uAgent at:', UAGENT_BASE_URL);

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
    // Use the uAgent's built-in /submit endpoint for communication
    const response = await axios.post(
      `${UAGENT_BASE_URL}/submit`,
      {
        // Format the message according to the uAgent protocol
        sender: 'frontend-client',
        destination: 'emrys-defi-agent',
        message: {
          protocol_name: protocolName,
        },
      },
      {
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000, // 10 second timeout
      },
    );

    console.log('Protocol info response:', response.data);

    if (response.data && response.data.information) {
      return response.data.information;
    } else if (response.data && response.data.results) {
      // Handle responses from the DeFiProtocolResponse format
      return response.data.results;
    } else {
      throw new Error('Invalid protocol response format');
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
    // For simplicity, return a static list of protocols
    // In a production environment, we would use the uAgent's message system
    return {
      timestamp: Date.now(),
      protocols: {
        SOON_SVM: 'SOON SVM',
        IBC: 'IBC',
        WALRUS: 'Walrus',
        ZPL: 'ZPL UTXO Bridge',
      },
      count: 4,
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
