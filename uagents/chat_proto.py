from datetime import datetime
from uuid import uuid4
from typing import Any

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

from model import get_protocol_info, DeFiProtocolRequest

#Replace the AI Agent Address with anyone of the following LLMs as they support StructuredOutput required for the processing of this agent. 

AI_AGENT_ADDRESS = 'agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y'

if not AI_AGENT_ADDRESS:
    raise ValueError("AI_AGENT_ADDRESS not set")


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
                    "Welcome to the Emrys Blockchain Technology Assistant! I can provide educational information about technologies used in the Emrys ecosystem: Solana, SVM, Soon SVM, Walrus, UTXO model, IBC protocol, ZPL UTXO Bridge, WalletConnect Integration, and Mainnet Deployment. What would you like to learn about?",
                    end_session=False
                )
            )
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Got a message from {sender}: {item.text}")
            ctx.storage.set(str(ctx.session), sender)
            await ctx.send(
                AI_AGENT_ADDRESS,
                StructuredOutputPrompt(
                    prompt=item.text, output_schema=DeFiProtocolRequest.schema()
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

    if "<UNKNOWN>" in str(msg.output):
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't understand which technology you're asking about. Please try asking about one of these: Solana, SVM, Soon SVM, Walrus, UTXO, IBC, ZPL UTXO Bridge, WalletConnect Integration, or Mainnet Deployment."
            ),
        )
        return

    prompt = DeFiProtocolRequest.parse_obj(msg.output)

    try:
        protocol_info = await get_protocol_info(prompt.protocol_name)
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't process your technology information request. Please try again later."
            ),
        )
        return

    if "not found" in protocol_info:
        await ctx.send(session_sender, create_text_chat(protocol_info))
        return

    chat_message = create_text_chat(protocol_info)

    await ctx.send(session_sender, chat_message)