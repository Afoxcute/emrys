import os
from enum import Enum

from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from chat_proto import chat_proto, struct_output_client_proto
from model import get_protocol_info, DeFiProtocolRequest, DeFiProtocolResponse

agent = Agent()

proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="Emrys-Technology-Education-Protocol",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=30),
)

@proto.on_message(
    DeFiProtocolRequest, replies={DeFiProtocolResponse, ErrorMessage}
)
async def handle_request(ctx: Context, sender: str, msg: DeFiProtocolRequest):
    ctx.logger.info(f"Received technology info request for {msg.protocol_name}")
    try:
        results = await get_protocol_info(msg.protocol_name)
        ctx.logger.info(f'Retrieved information for {msg.protocol_name}')
        ctx.logger.info("Successfully fetched technology information")
        await ctx.send(sender, DeFiProtocolResponse(results=results))
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))

agent.include(proto, publish_manifest=True)

### Health check related code
def agent_is_healthy() -> bool:
    """
    Implement the actual health check logic here.
    Check if the agent can retrieve technology information.
    """
    try:
        import asyncio
        asyncio.run(get_protocol_info("solana"))
        return True
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
        await ctx.send(sender, AgentHealth(agent_name="emrys_technology_agent", status=status))

agent.include(health_protocol, publish_manifest=True)
agent.include(chat_proto, publish_manifest=True)
agent.include(struct_output_client_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run() 