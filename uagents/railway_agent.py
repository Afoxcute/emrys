import time
import os
from typing import Any, Dict, Optional, List
from enum import Enum

# Try to load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from uagents import Agent, Context, Model
from model import get_protocol_info, get_tokens_info, get_faq_response, BLOCKCHAIN_TECHNOLOGIES

# Define models for requests and responses
class ProtocolInfoRequest(Model):
    protocol_name: Optional[str] = None
    protocolName: Optional[str] = None

class ProtocolInfoResponse(Model):
    timestamp: int
    protocol_name: str
    information: str
    agent_address: str

class ChatRequest(Model):
    question: str
    
class ChatResponse(Model):
    timestamp: int
    answer: str
    suggested_questions: Optional[List[str]] = None
    agent_address: str

# Create the agent with environment variables for Railway deployment
PORT = int(os.environ.get("PORT", 8000))
SEED = os.environ.get("AGENT_SEED", "emrys_protocol_info_agent_seed")
ENDPOINT = os.environ.get("AGENT_ENDPOINT", f"http://localhost:{PORT}/submit")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

agent = Agent(
    name="Protocol Info Agent",
    seed=SEED,
    port=PORT,
    endpoint=[ENDPOINT],
    log_level=LOG_LEVEL
)

# Configure CORS middleware for the agent
@agent.middleware
async def cors_middleware(request, handler):
    """
    CORS middleware to allow requests from any origin
    Required to respond to browser-based requests
    """
    orig_response = await handler(request)

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    }

    # If original response has headers, preserve them
    if hasattr(orig_response, "headers"):
        for name, value in headers.items():
            orig_response.headers[name] = value
        return orig_response
    
    return orig_response

@agent.on_rest_get("/health", Model)
async def handle_health_check(ctx: Context) -> Dict[str, Any]:
    """
    Health check endpoint to verify that the agent is running
    """
    return {
        "status": "healthy",
        "timestamp": int(time.time()),
        "agent_address": ctx.agent.address,
    }

@agent.on_rest_post("/protocol/info", ProtocolInfoRequest, ProtocolInfoResponse)
async def handle_protocol_info(ctx: Context, req: ProtocolInfoRequest) -> ProtocolInfoResponse:
    """
    Endpoint to retrieve information about a specific blockchain protocol
    """
    # Handle both naming conventions (camelCase from JS, snake_case from Python)
    protocol_name = req.protocol_name or req.protocolName or ""
    
    ctx.logger.info(f"Received request for protocol: {protocol_name}")
    
    protocol_info = await get_protocol_info(protocol_name)
    
    return ProtocolInfoResponse(
        timestamp=int(time.time()),
        protocol_name=protocol_name,
        information=protocol_info,
        agent_address=ctx.agent.address,
    )

@agent.on_rest_get("/protocols/list", Model)
async def handle_list_protocols(ctx: Context) -> Dict[str, Any]:
    """
    Endpoint to list all available blockchain protocols
    """
    protocols = {
        "bitcoin": "Bitcoin cryptocurrency",
        "ethereum": "Ethereum smart contract platform",
        "solana": "Solana high-performance blockchain",
        "polkadot": "Polkadot multi-chain network",
        "avalanche": "Avalanche consensus protocol",
        "cardano": "Cardano proof-of-stake blockchain",
        "cosmos": "Cosmos blockchain ecosystem",
        "near": "NEAR Protocol",
        "fantom": "Fantom Opera network",
    }
    
    return {
        "timestamp": int(time.time()),
        "protocols": protocols,
        "count": len(protocols),
    }

@agent.on_rest_post("/chat/faq", ChatRequest, ChatResponse)
async def handle_faq_question(ctx: Context, req: ChatRequest) -> ChatResponse:
    """
    Endpoint to handle FAQ questions from the chat interface
    """
    ctx.logger.info(f"Received FAQ question: {req.question}")
    
    # Get response from the FAQ function in model.py
    answer, suggested_questions = await get_faq_response(req.question)
    
    return ChatResponse(
        timestamp=int(time.time()),
        answer=answer,
        suggested_questions=suggested_questions,
        agent_address=ctx.agent.address,
    )

@agent.on_rest_get("/tokens/info", Model)
async def handle_tokens_info(ctx: Context) -> Dict[str, Any]:
    """
    Endpoint to list supported tokens and their information
    """
    tokens_info = await get_tokens_info()
    
    return {
        "timestamp": int(time.time()),
        "tokens": tokens_info,
        "count": len(tokens_info),
    }

if __name__ == "__main__":
    print(f"Starting Protocol Info Agent on port {PORT}")
    print(f"Health check available at: http://localhost:{PORT}/health")
    print(f"Protocol list available at: http://localhost:{PORT}/protocols/list")
    print(f"Protocol info endpoint: http://localhost:{PORT}/protocol/info")
    print(f"CORS is enabled for all origins")
    agent.run() 