import os
from enum import Enum
import json
import time
from pydantic import BaseModel

from uagents import Agent, Context, Model, Protocol
from uagents.setup import fund_agent_if_low
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.http import getMCPHttpServer, DefaultHandler, Response, Request, http_endpoint
from uagents_core.models import ErrorMessage

from chat_proto import chat_proto, struct_output_client_proto
from defi_protocol import get_defi_protocol_info, DeFiProtocolRequest, DeFiProtocolResponse, DEFI_PROTOCOLS

# Get environment variables or use defaults
AGENT_NAME = os.getenv("UAGENT_NAME", "emrys-defi-agent")

# Get port from Railway's PORT environment variable or use default 8080
PORT = int(os.getenv("PORT", "8080"))

# Use the provided Railway URL with fallbacks
RAILWAY_URL = os.getenv("RAILWAY_URL", "emrys-production.up.railway.app")

# Construct the endpoint URL
if not RAILWAY_URL.startswith(("http://", "https://")):
    RAILWAY_URL = f"https://{RAILWAY_URL}"
AGENT_ENDPOINT = f"{RAILWAY_URL}/submit"

print(f"Agent endpoint configured as: {AGENT_ENDPOINT}")
print(f"Agent will run on port: {PORT}")

# Create agent with proper configuration
agent = Agent(
    name=AGENT_NAME,
    port=PORT,  # Set the port during agent initialization
    endpoint=[AGENT_ENDPOINT],  # Register endpoint so agent is reachable
)

# Create protocol for DeFi protocol information
proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Emrys-Solana-Cosmos-DeFi-Protocol-Education",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=30),
)

# Create REST endpoint-specific models
class ProtocolInfoRequest(BaseModel):
    protocolName: str

class ProtocolInfoResponse(BaseModel):
    timestamp: int
    protocolName: str
    information: str
    agent_address: str

class ProtocolsListResponse(BaseModel):
    timestamp: int
    protocols: dict
    count: int

# Define HTTP endpoints using the uagents http_endpoint decorator
@http_endpoint("GET", "/health")
async def health_check(request: Request) -> Response:
    return Response(status=200, body={"status": "ok"})

@http_endpoint("POST", "/protocol/info")
async def protocol_info(request: Request) -> Response:
    try:
        data = await request.json()
        protocol_name = data.get("protocolName")
        
        if not protocol_name:
            return Response(status=400, body={"error": "Protocol name is required"})
            
        # Get protocol info using existing function
        information = await get_defi_protocol_info(protocol_name)
        
        # Return structured response
        result = {
            "timestamp": int(time.time()),
            "protocolName": protocol_name,
            "information": information,
            "agent_address": agent.address
        }
        
        return Response(status=200, body=result)
    except Exception as e:
        return Response(status=404, body={"error": f"Protocol not found: {str(e)}"})

@http_endpoint("GET", "/protocols/list")
async def protocols_list(request: Request) -> Response:
    # Extract all protocols from DEFI_PROTOCOLS dictionary
    protocols = {k: v.get("name", k) for k, v in DEFI_PROTOCOLS.items()}
    
    result = {
        "timestamp": int(time.time()),
        "protocols": protocols,
        "count": len(protocols)
    }
    
    return Response(status=200, body=result)

@proto.on_message(
    DeFiProtocolRequest, replies={DeFiProtocolResponse, ErrorMessage}
)
async def handle_request(ctx: Context, sender: str, msg: DeFiProtocolRequest):
    ctx.logger.info(f"Received DeFi protocol info request for {msg.protocol_name}")
    try:
        results = await get_defi_protocol_info(msg.protocol_name)
        ctx.logger.info(f'Retrieved information for {msg.protocol_name}')
        ctx.logger.info("Successfully fetched DeFi protocol information")
        await ctx.send(sender, DeFiProtocolResponse(results=results))
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))

# Include the protocols in the agent
agent.include(proto, publish_manifest=True)
agent.include(chat_proto, publish_manifest=True)
agent.include(struct_output_client_proto, publish_manifest=True)

# Setup HTTP server with our endpoints
http_server = getMCPHttpServer(agent, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    print(f"Starting agent with endpoint {AGENT_ENDPOINT}")
    print(f"HTTP API available at http://0.0.0.0:{PORT}")
    
    # Fund the agent if it's low on funds (optional)
    fund_agent_if_low(agent.wallet.address())
    
    # Run the agent with the HTTP server
    agent.run(http_server=http_server) 