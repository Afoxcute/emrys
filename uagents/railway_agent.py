import time
import os
from typing import Any, Dict, Optional

# Try to load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uagents import Agent, Context, Model
from model import get_protocol_info, BLOCKCHAIN_TECHNOLOGIES

# Define models for requests and responses
class ProtocolInfoRequest(Model):
    protocol_name: Optional[str] = None
    protocolName: Optional[str] = None

class ProtocolInfoResponse(Model):
    timestamp: int
    protocol_name: str
    information: str
    agent_address: str

class ChatQuestionRequest(Model):
    question: str

class ChatQuestionResponse(Model):
    timestamp: int
    question: str
    answer: str
    agent_address: str

# Create the agent with environment variables for Railway deployment
PORT = int(os.environ.get("PORT", 8000))
SEED = os.environ.get("AGENT_SEED", "emrys_protocol_info_agent_seed")
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# Create a FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the agent
agent = Agent(
    name="Protocol Info Agent",
    seed=SEED,
    port=PORT,
    endpoint=[f"{BASE_URL}/submit"],
    log_level=LOG_LEVEL
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": int(time.time()),
        "agent_name": agent.name,
        "agent_address": agent.address,
    }

# Protocol info endpoint
@app.post("/protocol/info", response_model=ProtocolInfoResponse)
async def protocol_info(req: ProtocolInfoRequest):
    # Use either protocol_name or protocolName, preferring protocolName if provided
    protocol_name = req.protocolName if req.protocolName is not None else req.protocol_name
    if not protocol_name:
        raise ValueError("Protocol name is required")
    
    print(f"Received protocol info request for: {protocol_name}")
    
    # Get protocol information using the existing function
    info = await get_protocol_info(protocol_name)
    
    return ProtocolInfoResponse(
        timestamp=int(time.time()),
        protocol_name=protocol_name,
        information=info,
        agent_address=agent.address
    )

# Protocols list endpoint
@app.get("/protocols/list")
async def list_protocols():
    print("Protocol list requested")
    protocols = {key: tech.get('name', key) for key, tech in BLOCKCHAIN_TECHNOLOGIES.items()}
    
    return {
        "timestamp": int(time.time()),
        "protocols": protocols,
        "count": len(protocols)
    }

# Chat question endpoint
@app.post("/chat/question", response_model=ChatQuestionResponse)
async def chat_question(req: ChatQuestionRequest):
    """
    Endpoint to handle chat questions and provide responses.
    """
    question = req.question
    if not question:
        raise ValueError("Question is required")

    print(f"Received chat question: {question}")
    
    # Generate response based on the question
    # First check if it's about a specific blockchain protocol
    words = question.lower().split()
    common_protocols = ["ethereum", "solana", "bitcoin", "polygon", "avalanche", "cosmos", "polkadot"]
    
    for word in words:
        if word in common_protocols:
            try:
                answer = await get_protocol_info(word)
                return ChatQuestionResponse(
                    timestamp=int(time.time()),
                    question=question,
                    answer=answer,
                    agent_address=agent.address,
                )
            except Exception as e:
                print(f"Error getting protocol info: {e}")
                break
    
    # Otherwise, provide a general response based on keywords
    if any(word in question.lower() for word in ["bridge", "transfer", "send"]):
        answer = "Emrys bridge allows you to transfer tokens between different blockchains quickly and securely. Just select your source and destination chains, the token, and the amount you want to transfer, and we'll handle the rest!"
    elif any(word in question.lower() for word in ["wallet", "connect"]):
        answer = "To use Emrys bridge, you'll need to connect a compatible wallet for both your source and destination chains. We support multiple wallet providers including MetaMask, Phantom, and others."
    elif any(word in question.lower() for word in ["fee", "cost", "price"]):
        answer = "Fees on Emrys bridge vary depending on the source and destination chains. You'll see a detailed breakdown of all fees before you confirm your transaction, including gas fees and interchain fees."
    elif any(word in question.lower() for word in ["security", "safe", "secure"]):
        answer = "Security is our top priority at Emrys. We use advanced cryptographic techniques and have undergone rigorous security audits to ensure your assets are protected throughout the bridging process."
    elif any(word in question.lower() for word in ["time", "duration", "long", "wait"]):
        answer = "Most transfers on Emrys complete within a few minutes, but the exact time can vary depending on network conditions and the chains involved. You can track the status of your transfer in real-time."
    elif any(word in question.lower() for word in ["walrus", "storage"]):
        answer = "Walrus is our decentralized storage solution that securely stores transaction data across multiple networks. It ensures your cross-chain transaction data remains secure, immutable, and easily accessible at all times."
    elif any(word in question.lower() for word in ["token", "asset", "cryptocurrency"]):
        answer = "Emrys supports bridging of native tokens (like ETH, AVAX, SOL) and popular token standards like USDC and USDT. We're constantly adding support for more tokens."
    else:
        answer = "I'm here to help you navigate Emrys bridge! You can ask me about supported chains, tokens, fees, security, or any other aspect of our cross-chain bridge. If you have a technical issue, please contact our support team."
    
    return ChatQuestionResponse(
        timestamp=int(time.time()),
        question=question,
        answer=answer,
        agent_address=agent.address,
    )

if __name__ == "__main__":
    print(f"Starting Protocol Info Agent on port {PORT}")
    print(f"Health check available at: {BASE_URL}/health")
    print(f"Protocol list available at: {BASE_URL}/protocols/list")
    print(f"Protocol info endpoint: {BASE_URL}/protocol/info")
    print(f"Chat question endpoint: {BASE_URL}/chat/question")
    print(f"CORS is enabled for all origins")
    
    # Run with uvicorn directly
    uvicorn.run(app, host="0.0.0.0", port=PORT) 