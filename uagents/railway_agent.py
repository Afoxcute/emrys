import time
import os
from typing import Any, Dict, Optional

# Try to load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

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
ENDPOINT = os.environ.get("AGENT_ENDPOINT", f"http://emrys-production.up.railway.app:8080/submit")
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
    """Add CORS headers to all responses."""
    response = await handler(request)
    
    # Add CORS headers
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    # Handle preflight requests
    if request.method == "OPTIONS":
        return response
    
    return response

@agent.on_rest_get("/health", Model)
async def handle_health_check(ctx: Context) -> Dict[str, Any]:
    """Health check endpoint for monitoring."""
    ctx.logger.info("Health check requested")
    return {
        "status": "healthy",
        "timestamp": int(time.time())
    }

@agent.on_rest_post("/protocol/info", ProtocolInfoRequest, ProtocolInfoResponse)
async def handle_protocol_info(ctx: Context, req: ProtocolInfoRequest) -> ProtocolInfoResponse:
    """Endpoint to get information about a specific DeFi protocol."""
    # Use either protocol_name or protocolName, preferring protocolName if provided
    protocol_name = req.protocolName if req.protocolName is not None else req.protocol_name
    ctx.logger.info(f"Received protocol info request for: {protocol_name}")
    
    # Get protocol information using the existing function
    info = await get_protocol_info(protocol_name)
    
    return ProtocolInfoResponse(
        timestamp=int(time.time()),
        protocol_name=protocol_name,
        information=info,
        agent_address=ctx.agent.address
    )

@agent.on_rest_get("/protocols/list", Model)
async def handle_list_protocols(ctx: Context) -> Dict[str, Any]:
    """Endpoint to list all available protocols."""
    ctx.logger.info("Protocol list requested")
    protocols = {key: tech.get('name', key) for key, tech in BLOCKCHAIN_TECHNOLOGIES.items()}
    
    return {
        "timestamp": int(time.time()),
        "protocols": protocols,
        "count": len(protocols)
    }

@agent.on_rest_post("/chat/question", ChatQuestionRequest, ChatQuestionResponse)
async def handle_chat_question(ctx: Context, req: ChatQuestionRequest) -> ChatQuestionResponse:
    """
    Endpoint to handle chat questions and provide responses.
    """
    question = req.question
    if not question:
        raise ValueError("Question is required")

    ctx.logger.info(f"Received chat question: {question}")
    
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
                    agent_address=ctx.agent.address,
                )
            except Exception as e:
                ctx.logger.error(f"Error getting protocol info: {e}")
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
        agent_address=ctx.agent.address,
    )

if __name__ == "__main__":
    print(f"Starting Protocol Info Agent on port {PORT}")
    print(f"Health check available at: http://emrys-production.up.railway.app:8080/health")
    print(f"Protocol list available at: http://emrys-production.up.railway.app:8080/protocols/list")
    print(f"Protocol info endpoint: http://emrys-production.up.railway.app:8080/protocol/info")
    print(f"CORS is enabled for all origins")
    agent.run() 