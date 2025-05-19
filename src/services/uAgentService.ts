import axios from 'axios';
import { logger } from '../utils/logger';

// Use the Railway URL for the uAgent
const UAGENT_BASE_URL =
  process.env.NEXT_PUBLIC_UAGENT_URL || 'https://emrys-production.up.railway.app';

console.log('Connecting to uAgent service at:', UAGENT_BASE_URL);

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
 * Fetch information about a specific blockchain protocol from the uAgent
 */
export async function fetchProtocolInfo(protocolName: string): Promise<string> {
  try {
    const response = await axios.post<ProtocolInfo>(`${UAGENT_BASE_URL}/protocol/info`, {
      protocolName: protocolName,
    });
    console.log('Protocol info response:', response.data);
    return response.data.information;
  } catch (error) {
    logger.error('Error fetching protocol info:', error);
    throw new Error('Failed to fetch protocol information');
  }
}

/**
 * Get list of all available protocols from the uAgent
 */
export async function fetchProtocolsList(): Promise<ProtocolsListResponse> {
  try {
    const response = await axios.get<ProtocolsListResponse>(`${UAGENT_BASE_URL}/protocols/list`);
    console.log('Protocols list response:', response.data);
    return response.data;
  } catch (error) {
    logger.error('Error fetching protocols list:', error);
    throw new Error('Failed to fetch protocols list');
  }
}

/**
 * Always returns true since we're assuming the agent is available
 */
export async function checkUAgentHealth(): Promise<boolean> {
  return true;
}
