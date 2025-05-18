import axios from 'axios';
import { logger } from '../utils/logger';

// Replace with your actual deployed Railway URL
const UAGENT_BASE_URL =
  process.env.NEXT_PUBLIC_UAGENT_URL || 'https://your-protocol-agent-production.up.railway.app';

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

export interface ChatResponse {
  timestamp: number;
  question: string;
  answer: string;
  agent_address: string;
}

/**
 * Send a user question to the uAgent and get a response
 */
export async function sendChatQuestion(question: string): Promise<string> {
  try {
    const response = await axios.post<ChatResponse>(`${UAGENT_BASE_URL}/chat/question`, {
      question,
    });
    return response.data.answer;
  } catch (error) {
    logger.error('Error sending chat question:', error);
    throw new Error('Failed to get answer from AI assistant');
  }
}

/**
 * Fetch information about a specific blockchain protocol from the uAgent
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
