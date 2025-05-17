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

if __name__ == "__main__":
    print(f"Starting Protocol Info Agent on port {PORT}")
    print(f"Health check available at: http://localhost:{PORT}/health")
    print(f"Protocol list available at: http://localhost:{PORT}/protocols/list")
    print(f"Protocol info endpoint: http://localhost:{PORT}/protocol/info")
    print(f"CORS is enabled for all origins")
    agent.run() 