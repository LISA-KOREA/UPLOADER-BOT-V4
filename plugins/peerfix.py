from pyrogram import Client
import logging

logger = logging.getLogger(__name__)


PEER_CACHE = set()

async def ensure_peer(client: Client, chat_id: int):
    if not isinstance(chat_id, int):
        raise ValueError(f"chat_id must be int, got {type(chat_id)}")

    if chat_id in PEER_CACHE:
        return

    try:
        await client.get_chat(chat_id)
        PEER_CACHE.add(chat_id)
        logger.info(f"✅ Peer loaded: {chat_id}")
    except Exception as e:
        logger.warning(f"⚠️ Peer not ready yet: {chat_id} | {e}")
        raise
