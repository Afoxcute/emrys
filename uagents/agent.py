import os
from enum import Enum
from typing import Dict, Any
import time

from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from chat_proto import chat_proto, struct_output_client_proto
from model import get_protocol_info, DeFiProtocolRequest, DeFiProtocolResponse, BLOCKCHAIN_TECHNOLOGIES

# Get environment variables for Railway deployment
PORT = int(os.environ.get("PORT", 8000))
HOST = os.environ.get("HOST", "0.0.0.0")
AGENT_SEED = os.environ.get("AGENT_SEED", "emrys_protocol_agent_seed_phrase")

# Configure the agent with port and endpoint for REST API
agent = Agent(
    name="EmrysProtocolAgent",
    port=PORT,
    endpoint=[f"http://{HOST}:{PORT}/submit"],
    seed=AGENT_SEED
)

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
    except Exception as e:
        agent.logger.error(f"Health check failed: {str(e)}")
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

# REST API Models
class ProtocolInfoRequest(Model):
    protocolName: str

class ProtocolInfoResponse(Model):
    timestamp: int
    protocolName: str
    information: str
    agent_address: str

class ProtocolsListResponse(Model):
    timestamp: int
    protocols: Dict[str, str]
    count: int

class HealthResponse(Model):
    status: str
    timestamp: int
    agent_name: str

# REST API endpoints
@agent.on_event("startup")
async def startup():
    agent.logger.info(f"Emrys Protocol Agent starting on {HOST}:{PORT}")
    agent.logger.info(f"REST endpoints available at http://{HOST}:{PORT}/")
    agent.logger.info(f"Health check endpoint: http://{HOST}:{PORT}/health")

@agent.on_rest_post("/protocol/info", ProtocolInfoRequest, ProtocolInfoResponse)
async def handle_protocol_info(ctx: Context, req: ProtocolInfoRequest) -> ProtocolInfoResponse:
    ctx.logger.info(f"REST API: Received request for protocol info: {req.protocolName}")
    try:
        info = await get_protocol_info(req.protocolName)
        return ProtocolInfoResponse(
            timestamp=int(time.time()),
            protocolName=req.protocolName,
            information=info,
            agent_address=ctx.agent.address
        )
    except Exception as err:
        ctx.logger.error(f"Error fetching protocol info: {err}")
        # Return error information in a structured way
        return ProtocolInfoResponse(
            timestamp=int(time.time()),
            protocolName=req.protocolName,
            information=f"Error: {str(err)}",
            agent_address=ctx.agent.address
        )

@agent.on_rest_get("/protocols/list", ProtocolsListResponse)
async def handle_protocols_list(ctx: Context) -> Dict[str, Any]:
    ctx.logger.info("REST API: Received request for protocols list")
    try:
        # Use the technologies from the BLOCKCHAIN_TECHNOLOGIES dictionary
        protocols = {key: tech['name'] for key, tech in BLOCKCHAIN_TECHNOLOGIES.items()}
        
        return {
            "timestamp": int(time.time()),
            "protocols": protocols,
            "count": len(protocols)
        }
    except Exception as err:
        ctx.logger.error(f"Error fetching protocols list: {err}")
        return {
            "timestamp": int(time.time()),
            "protocols": {},
            "count": 0
        }

@agent.on_rest_get("/health", HealthResponse)
async def handle_health(ctx: Context) -> Dict[str, Any]:
    ctx.logger.info("REST API: Received health check request")
    try:
        is_healthy = agent_is_healthy()
        status = "healthy" if is_healthy else "unhealthy"
    except Exception as err:
        ctx.logger.error(f"Error checking health: {err}")
        status = "unhealthy"
    
    return {
        "status": status,
        "timestamp": int(time.time()),
        "agent_name": "emrys_technology_agent"
    }

if __name__ == "__main__":
    # Run the agent with default settings
    agent.run() 