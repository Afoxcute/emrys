import axios from 'axios';
import { logger } from '../utils/logger';

// Use Railway URL for uAgent
const UAGENT_BASE_URL = process.env.NEXT_PUBLIC_UAGENT_URL || 'https://emrys-production.up.railway.app';

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
    const response = await axios.post<ProtocolInfo>(
      `${UAGENT_BASE_URL}/protocol/info`,
      { protocolName },
      {
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000, // 10 second timeout
      }
    );
    
    console.log('Protocol info response:', response.data);
    
    if (response.data && response.data.information) {
      return response.data.information;
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
    const response = await axios.get<ProtocolsListResponse>(
      `${UAGENT_BASE_URL}/protocols/list`,
      {
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000, // 10 second timeout
      }
    );
    
    console.log('Protocols list response:', response.data);
    
    if (response.data && response.data.protocols) {
      return response.data;
    } else {
      throw new Error('Invalid protocols list response format');
    }
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
  try {
    // Check health endpoint
    const response = await axios.get<{status: string}>(
      `${UAGENT_BASE_URL}/health`,
      {
        timeout: 5000, // 5 second timeout
      }
    );
    
    // Check if the response has status "ok"
    return response.data?.status === 'ok';
  } catch (error) {
    logger.error('Health check failed:', error);
    // Return true to assume the agent is always available, as requested
    return true;
  }
}
