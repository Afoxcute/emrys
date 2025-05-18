import axios from 'axios';
import { logger } from '../utils/logger';

// Get the uAgent base URL from environment variables with a fallback to localhost for development
const UAGENT_BASE_URL = process.env.NEXT_PUBLIC_UAGENT_URL || 'http://localhost:8000';

/**
 * Response interface for protocol information
 *
 * @endpoint POST /protocol/info
 * @request { protocolName: string }
 */
export interface ProtocolInfo {
  timestamp: number;
  protocolName: string;
  information: string;
  agent_address: string;
}

/**
 * Response interface for protocols list
 *
 * @endpoint GET /protocols/list
 */
export interface ProtocolsListResponse {
  timestamp: number;
  protocols: Record<string, string>;
  count: number;
}

/**
 * Fetch information about a specific blockchain protocol from the uAgent
 *
 * @endpoint POST /protocol/info
 * @example
 * const info = await fetchProtocolInfo('solana');
 */
export async function fetchProtocolInfo(protocolName: string): Promise<string> {
  try {
    const response = await axios.post<ProtocolInfo>(`${UAGENT_BASE_URL}/protocol/info`, {
      protocolName: protocolName,
    });
    return response.data.information;
  } catch (error) {
    logger.error('Error fetching protocol info:', error);
    throw new Error('Failed to fetch protocol information');
  }
}

/**
 * Get list of all available protocols from the uAgent
 *
 * @endpoint GET /protocols/list
 * @example
 * const protocols = await fetchProtocolsList();
 */
export async function fetchProtocolsList(): Promise<ProtocolsListResponse> {
  try {
    const response = await axios.get<ProtocolsListResponse>(`${UAGENT_BASE_URL}/protocols/list`);
    return response.data;
  } catch (error) {
    logger.error('Error fetching protocols list:', error);
    throw new Error('Failed to fetch protocols list');
  }
}

/**
 * Check if the uAgent service is healthy
 *
 * @endpoint GET /health
 * @example
 * const isHealthy = await checkUAgentHealth();
 */
export async function checkUAgentHealth(): Promise<boolean> {
  try {
    const response = await axios.get(`${UAGENT_BASE_URL}/health`);
    return response.data.status === 'healthy';
  } catch (error) {
    logger.error('Error checking uAgent health:', error);
    return false;
  }
}
