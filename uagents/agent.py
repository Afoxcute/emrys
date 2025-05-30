import os
from enum import Enum
import json
import time
from pydantic import BaseModel

from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
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

# Create agent with proper configuration
agent = Agent(
    name=AGENT_NAME,
    port=PORT,
    endpoint=[AGENT_ENDPOINT],
)

# Create protocol for DeFi protocol information
proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Emrys-Solana-Cosmos-DeFi-Protocol-Education",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=30),
)

# Create protocol info request/response models for agent messaging
class ProtocolInfoRequest(Model):
    protocol_name: str

class ProtocolInfoResponse(Model):
    timestamp: int
    protocol_name: str
    information: str
    agent_address: str

class ProtocolsListRequest(Model):
    pass

class ProtocolsListResponse(Model):
    timestamp: int
    protocols: dict
    count: int

# Define health check endpoint handler
@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("Agent started successfully")

# Define protocol info endpoint handler
@proto.on_message(ProtocolInfoRequest, replies={ProtocolInfoResponse, ErrorMessage})
async def get_protocol_info(ctx: Context, sender: str, msg: ProtocolInfoRequest):
    ctx.logger.info(f"Received protocol info request for {msg.protocol_name}")
    try:
        information = await get_defi_protocol_info(msg.protocol_name)
        ctx.logger.info(f"Retrieved information for {msg.protocol_name}")
        
        response = ProtocolInfoResponse(
            timestamp=int(time.time()),
            protocol_name=msg.protocol_name,
            information=information,
            agent_address=agent.address
        )
        
        await ctx.send(sender, response)
    except Exception as err:
        ctx.logger.error(f"Error retrieving protocol info: {err}")
        await ctx.send(sender, ErrorMessage(error=str(err)))

# Define protocols list endpoint handler
@proto.on_message(ProtocolsListRequest, replies={ProtocolsListResponse})
async def get_protocols_list(ctx: Context, sender: str, msg: ProtocolsListRequest):
    ctx.logger.info("Received protocols list request")
    
    # Extract all protocols from DEFI_PROTOCOLS dictionary
    protocols = {k: v.get("name", k) for k, v in DEFI_PROTOCOLS.items()}
    
    response = ProtocolsListResponse(
        timestamp=int(time.time()),
        protocols=protocols,
        count=len(protocols)
    )
    
    await ctx.send(sender, response)

# Original DeFi protocol info request handler
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
    
    # Fund the agent if it's low on funds (optional)
    fund_agent_if_low(agent.wallet.address())
    
    # Run the agent
    agent.run() 