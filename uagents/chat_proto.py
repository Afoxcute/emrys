from datetime import datetime, timedelta
from uuid import uuid4
from typing import Any
import time

from uagents import Context, Model, Protocol

#Import the necessary components of the chat protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

from defi_protocol import get_defi_protocol_info, DeFiProtocolRequest

# OpenAI LLM Agent address for structured output
OPENAI_AGENT_ADDRESS = 'agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y'

if not OPENAI_AGENT_ADDRESS:
    raise ValueError("OPENAI_AGENT_ADDRESS not set")

# Configuration constants
RESPONSE_TIMEOUT_SECONDS = 15  # Time to wait for OpenAI response before providing fallback

# Rate limiting implementation
class RateLimiter:
    def __init__(self, requests_per_hour=6):
        self.requests_per_hour = requests_per_hour
        self.request_times = []
        
    async def check_rate_limit(self, ctx: Context) -> bool:
        """Check if we're within rate limits (6 requests per hour)"""
        current_time = time.time()
        # Remove requests older than 1 hour
        self.request_times = [t for t in self.request_times if current_time - t < 3600]
        
        if len(self.request_times) >= self.requests_per_hour:
            ctx.logger.warning(f"Rate limit exceeded: {len(self.request_times)} requests in the last hour")
            return False
        
        # Add current request time
        self.request_times.append(current_time)
        return True

# Initialize rate limiter
rate_limiter = RateLimiter()

def create_text_chat(text: str, end_session: bool = True) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )


chat_proto = Protocol(spec=chat_protocol_spec)
struct_output_client_proto = Protocol(
    name="StructuredOutputClientProtocol", version="0.1.0"
)


class StructuredOutputPrompt(Model):
    prompt: str
    output_schema: dict[str, Any]


class StructuredOutputResponse(Model):
    output: dict[str, Any]


@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Got a message from {sender}: {msg.content[0].text}")
    ctx.storage.set(str(ctx.session), sender)
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id),
    )

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Got a start session message from {sender}")
            await ctx.send(
                sender,
                create_text_chat(
                    "Welcome to the Emrys Bridge Technology Assistant! I can provide comprehensive information about our cross-chain technologies including: SOON SVM (our enhanced Solana VM for high-throughput bridging), IBC protocol implementation, Walrus decentralized storage, ZPL UTXO Bridge (connecting Bitcoin, Dogecoin, and Litecoin to Solana), and various DeFi protocols in the Solana and Cosmos ecosystems. What would you like to learn about?",
                    end_session=False
                )
            )
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Got a message from {sender}: {item.text}")
            
            # Check rate limits before proceeding
            if not await rate_limiter.check_rate_limit(ctx):
                await ctx.send(
                    sender,
                    create_text_chat(
                        "Sorry, we've reached our query limit (6 requests per hour). Please try again later."
                    )
                )
                continue
                
            ctx.storage.set(str(ctx.session), sender)
            ctx.storage.set(f"{str(ctx.session)}_query", item.text)
            
            # Record the time we sent the request to OpenAI
            request_time = datetime.utcnow()
            ctx.storage.set(f"{str(ctx.session)}_request_time", request_time.isoformat())
            
            # Schedule a fallback response in case OpenAI doesn't respond in time
            ctx.storage.set(f"{str(ctx.session)}_fallback_scheduled", "true")
            
            # Add to active sessions list
            active_sessions = ctx.storage.get("active_sessions") or ""
            session_ids = [s.strip() for s in active_sessions.split(",") if s.strip()]
            if str(ctx.session) not in session_ids:
                session_ids.append(str(ctx.session))
                ctx.storage.set("active_sessions", ",".join(session_ids))
            
            # Send to OpenAI LLM for processing with structured output
            await ctx.send(
                OPENAI_AGENT_ADDRESS,
                StructuredOutputPrompt(
                    prompt=f"""Analyze this user query about blockchain technology: '{item.text}'
                    
Extract the specific DeFi protocol or blockchain technology the user is asking about. I need to return information about a single technology or protocol.

If the query mentions multiple technologies, select the primary one that seems to be the main focus.
If the query is vague or doesn't mention a specific technology, identify the most relevant technology based on context.

Available technologies include:
- Core technologies: SOON SVM, IBC, Walrus Storage, ZPL UTXO Bridge
- Solana protocols: Solend, Orca, Raydium, Serum, Marinade, Jito, Jupiter, Mango, Drift
- Cosmos protocols: Osmosis, Astroport, Mars, Neutron
- Cross-ecosystem: Wormhole, Pyth, LayerZero

The response should be formatted to match the DeFiProtocolRequest schema with a protocol_name field containing just the name of the protocol or technology.
""",
                    output_schema=DeFiProtocolRequest.schema()
                ),
            )
        else:
            ctx.logger.info(f"Got unexpected content from {sender}")


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(
        f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}"
    )


@struct_output_client_proto.on_message(StructuredOutputResponse)
async def handle_structured_output_response(
    ctx: Context, sender: str, msg: StructuredOutputResponse
):
    session_sender = ctx.storage.get(str(ctx.session))
    if session_sender is None:
        ctx.logger.error(
            "Discarding message because no session sender found in storage"
        )
        return

    # Cancel the fallback response since we got a response from OpenAI
    ctx.storage.set(f"{str(ctx.session)}_fallback_scheduled", "false")
    
    # Remove from active sessions
    active_sessions = ctx.storage.get("active_sessions") or ""
    session_ids = [s.strip() for s in active_sessions.split(",") if s.strip()]
    if str(ctx.session) in session_ids:
        session_ids.remove(str(ctx.session))
        ctx.storage.set("active_sessions", ",".join(session_ids))

    original_query = ctx.storage.get(f"{str(ctx.session)}_query") or "unknown query"
    ctx.logger.info(f"Processing structured output for query: {original_query}")

    # Store response for analytics and debugging
    ctx.storage.set(f"{str(ctx.session)}_openai_response", str(msg.output))

    if "<UNKNOWN>" in str(msg.output) or "error" in str(msg.output).lower():
        error_message = "I couldn't identify a specific protocol or technology in your question"
        
        if "error" in str(msg.output).lower():
            ctx.logger.error(f"OpenAI error: {str(msg.output)}")
            error_message = "Sorry, the AI service is currently experiencing issues. Please try again later."
        
        await ctx.send(
            session_sender,
            create_text_chat(
                f"{error_message}. You can ask about our core bridge technologies (SOON SVM, IBC, Walrus, ZPL UTXO Bridge), Solana protocols (Solend, Orca, Raydium, etc.), Cosmos protocols (Osmosis, Astroport, etc.), or cross-ecosystem bridges (Wormhole, Pyth)."
            ),
        )
        return

    try:
        prompt = DeFiProtocolRequest.parse_obj(msg.output)
        extracted_name = prompt.protocol_name.strip()
        ctx.logger.info(f"Extracted protocol name: {extracted_name}")
        
        # Store the extracted protocol name for analytics
        ctx.storage.set(f"{str(ctx.session)}_extracted_protocol", extracted_name)
        
        if not extracted_name:
            raise ValueError("Empty protocol name extracted")
            
        protocol_info = await get_defi_protocol_info(extracted_name)
    except Exception as err:
        ctx.logger.error(f"Error processing protocol info: {err}")
        
        # Check if it's a parsing error or a protocol info error
        error_type = "parsing error" if "parse_obj" in str(err) else "protocol info error"
        ctx.logger.error(f"Type of error: {error_type}")
        
        await ctx.send(
            session_sender,
            create_text_chat(
                f"Sorry, I encountered an error while processing information about '{prompt.protocol_name if 'prompt' in locals() else 'the requested technology'}'. Please try a different query or be more specific."
            ),
        )
        return

    if "not found" in protocol_info:
        # Try to provide a helpful response based on the original query
        context_response = f"I couldn't find specific information about '{prompt.protocol_name}'. {protocol_info}"
        await ctx.send(session_sender, create_text_chat(context_response))
        return

    # Store successful result for analytics
    ctx.storage.set(f"{str(ctx.session)}_success", "true")
    
    chat_message = create_text_chat(protocol_info)
    await ctx.send(session_sender, chat_message)


# Periodic task to check for timeout and send fallback responses
@chat_proto.on_interval(period=5.0)  # Check every 5 seconds
async def check_for_timeouts(ctx: Context):
    """Check for requests that haven't received a response within the timeout period"""
    now = datetime.utcnow()
    
    try:
        # Instead of trying to iterate through all keys, we'll check for requests
        # that have set a specific identifier when they were scheduled
        active_sessions = ctx.storage.get("active_sessions") or ""
        session_ids = [s.strip() for s in active_sessions.split(",") if s.strip()]
        
        for session_id in session_ids:
            fallback_scheduled = ctx.storage.get(f"{session_id}_fallback_scheduled")
            
            if fallback_scheduled != "true":
                continue  # Skip if fallback not scheduled or already processed
                
            # Get the timestamp of the request
            request_time_str = ctx.storage.get(f"{session_id}_request_time")
            if not request_time_str:
                continue
                
            try:
                request_time = datetime.fromisoformat(request_time_str)
                time_elapsed = now - request_time
            except ValueError:
                ctx.logger.error(f"Invalid timestamp format: {request_time_str}")
                continue
            
            # If we've waited longer than the timeout, send a fallback response
            if time_elapsed > timedelta(seconds=RESPONSE_TIMEOUT_SECONDS):
                ctx.logger.warning(f"Request timeout for session {session_id}. Sending fallback response.")
                
                # Get the session sender and original query
                session_sender = ctx.storage.get(session_id)
                original_query = ctx.storage.get(f"{session_id}_query") or "unknown query"
                
                if session_sender:
                    # Mark as processed
                    ctx.storage.set(f"{session_id}_fallback_scheduled", "false")
                    ctx.storage.set(f"{session_id}_fallback_sent", "true")
                    
                    # Try to extract potential keywords from the query
                    keywords = extract_potential_keywords(original_query)
                    
                    if keywords:
                        fallback = f"I'm currently having trouble with my AI service. Based on your query about '{keywords}', you might want to check our documentation or try asking about specific protocols like Solend, Orca, or our core technologies like SOON SVM or Walrus Storage."
                    else:
                        fallback = "I'm currently having trouble with my AI service. Please try again later or ask about a specific protocol or technology by name."
                        
                    await ctx.send(
                        session_sender,
                        create_text_chat(fallback)
                    )
                    
                    # Remove from active sessions
                    updated_sessions = [s for s in session_ids if s != session_id]
                    ctx.storage.set("active_sessions", ",".join(updated_sessions))
    except Exception as e:
        ctx.logger.error(f"Error in timeout checker: {e}")


def extract_potential_keywords(query: str) -> str:
    """Extract potential keywords from a query to provide a more helpful fallback response"""
    # List of known important keywords to look for
    important_terms = [
        "SOON", "SVM", "IBC", "Walrus", "Storage", "ZPL", "UTXO", "Bridge",
        "Solana", "Cosmos", "Bitcoin", "Ethereum", "Dogecoin", "Litecoin",
        "Solend", "Orca", "Raydium", "Serum", "Marinade", "Jito", "Jupiter", 
        "Osmosis", "Astroport", "Wormhole", "Pyth"
    ]
    
    # Simple keyword extraction
    lowercase_query = query.lower()
    found_terms = []
    
    for term in important_terms:
        if term.lower() in lowercase_query:
            found_terms.append(term)
    
    if found_terms:
        return ", ".join(found_terms)
    return ""