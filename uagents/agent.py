import os
from enum import Enum

from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from chat_proto import chat_proto, struct_output_client_proto
from defi_protocol import get_defi_protocol_info, DeFiProtocolRequest, DeFiProtocolResponse

# Get environment variables or use defaults
AGENT_NAME = os.getenv("UAGENT_NAME", "emrys-defi-agent")
AGENT_PORT = int(os.getenv("UAGENT_PORT", "8000"))

# For Railway, we need to construct the proper endpoint URL
# Railway sets RAILWAY_PUBLIC_DOMAIN if you've set up a custom domain
# or RAILWAY_SERVICE_URL for the default URL
RAILWAY_URL = os.getenv("RAILWAY_PUBLIC_DOMAIN") or os.getenv("RAILWAY_SERVICE_URL")

if RAILWAY_URL:
    # Use the Railway-provided URL for the endpoint
    if not RAILWAY_URL.startswith(("http://", "https://")):
        RAILWAY_URL = f"https://{RAILWAY_URL}"
    AGENT_ENDPOINT = f"{RAILWAY_URL}/submit"
else:
    # Fallback for local development
    AGENT_ENDPOINT = os.getenv("UAGENT_ENDPOINT", f"http://0.0.0.0:{AGENT_PORT}/submit")

print(f"Agent endpoint configured as: {AGENT_ENDPOINT}")

# Create agent with proper configuration
agent = Agent(
    name=AGENT_NAME,
    port=AGENT_PORT,
    endpoint=[AGENT_ENDPOINT],  # Register endpoint so agent is reachable
)

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

agent.include(proto, publish_manifest=True)

### Health check related code
def agent_is_healthy() -> bool:
    """
    Implement the actual health check logic here.
    Check if the agent can retrieve Solana and Cosmos protocol information.
    """
    try:
        import asyncio
        # Test both a Solana protocol and a Cosmos protocol
        solana_result = asyncio.run(get_defi_protocol_info("solend"))
        cosmos_result = asyncio.run(get_defi_protocol_info("osmosis"))
        svm_result = asyncio.run(get_defi_protocol_info("svm"))
        return "Solend" in solana_result and "Osmosis" in cosmos_result and "SVM" in svm_result
    except Exception:
        return False

class HealthCheck(Model):
    pass

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"

class AgentHealth(Model):
    agent_name: str
    status: HealthStatus

health_protocol = QuotaProtocol(
    storage_reference=agent.storage, name="HealthProtocol", version="0.1.0"
)

@health_protocol.on_message(HealthCheck, replies={AgentHealth})
async def handle_health_check(ctx: Context, sender: str, msg: HealthCheck):
    status = HealthStatus.UNHEALTHY
    try:
        if agent_is_healthy():
            status = HealthStatus.HEALTHY
    except Exception as err:
        ctx.logger.error(err)
    finally:
        await ctx.send(sender, AgentHealth(agent_name=AGENT_NAME, status=status))

agent.include(health_protocol, publish_manifest=True)
agent.include(chat_proto, publish_manifest=True)
agent.include(struct_output_client_proto, publish_manifest=True)

if __name__ == "__main__":
    # Railway provides $PORT, we'll use it if available, otherwise use AGENT_PORT
    port = int(os.getenv("PORT", AGENT_PORT))
    
    print(f"Starting agent on port {port} with endpoint {AGENT_ENDPOINT}")
    
    # Run with just the port parameter (host is not supported)
    agent.run(port=port) 