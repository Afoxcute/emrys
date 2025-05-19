import os
from enum import Enum
import json
import time
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
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

# Create FastAPI app for HTTP endpoints
app = FastAPI()

# Create Pydantic model for protocol info request
class ProtocolInfoRequest(BaseModel):
    protocolName: str

# Create Pydantic model for protocol info response
class ProtocolInfoResponse(BaseModel):
    timestamp: int
    protocolName: str
    information: str
    agent_address: str

# Create Pydantic model for protocols list response
class ProtocolsListResponse(BaseModel):
    timestamp: int
    protocols: dict
    count: int

@app.post("/protocol/info", response_model=ProtocolInfoResponse)
async def protocol_info(request: ProtocolInfoRequest):
    try:
        # Get protocol info using existing function
        information = await get_defi_protocol_info(request.protocolName)
        
        # Return structured response
        return {
            "timestamp": int(time.time()),
            "protocolName": request.protocolName,
            "information": information,
            "agent_address": "emrys-agent"  # Will be set properly after agent initialization
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Protocol not found: {str(e)}")

@app.get("/protocols/list", response_model=ProtocolsListResponse)
async def protocols_list():
    # Extract all protocols from DEFI_PROTOCOLS dictionary
    protocols = {k: v.get("name", k) for k, v in DEFI_PROTOCOLS.items()}
    
    return {
        "timestamp": int(time.time()),
        "protocols": protocols,
        "count": len(protocols)
    }

# Create agent with proper configuration
# Pass port directly during initialization
agent = Agent(
    name=AGENT_NAME,
    port=PORT,  # Set the port during agent initialization
    endpoint=[AGENT_ENDPOINT],  # Register endpoint so agent is reachable
)

# Mount FastAPI to uAgent with the correct host and port
agent.include_http_app(app, host="0.0.0.0", port=PORT)

# Update the agent address in the protocol_info endpoint
@app.post("/protocol/info", response_model=ProtocolInfoResponse)
async def protocol_info_with_agent(request: ProtocolInfoRequest):
    try:
        # Get protocol info using existing function
        information = await get_defi_protocol_info(request.protocolName)
        
        # Return structured response with agent address
        return {
            "timestamp": int(time.time()),
            "protocolName": request.protocolName,
            "information": information,
            "agent_address": agent.address
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Protocol not found: {str(e)}")

# Create protocol for DeFi protocol information
proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Emrys-Solana-Cosmos-DeFi-Protocol-Education",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=30),
)

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

if __name__ == "__main__":
    print(f"Starting agent with endpoint {AGENT_ENDPOINT}")
    print(f"HTTP API available at http://0.0.0.0:{PORT}")
    
    # Call run() without parameters - the port is already set during initialization
    agent.run() 