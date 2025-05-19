import os
from enum import Enum

from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from chat_proto import chat_proto, struct_output_client_proto
from defi_protocol import get_defi_protocol_info, DeFiProtocolRequest, DeFiProtocolResponse

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
# Pass port directly during initialization
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
    
    # Call run() without parameters - the port is already set during initialization
    agent.run() 