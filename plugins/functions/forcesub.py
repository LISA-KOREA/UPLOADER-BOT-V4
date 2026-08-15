import os
import asyncio
from plugins.config import Config
from pyrogram import Client
from pyrogram import enums
from pyrogram.errors import FloodWait, UserNotParticipant, ChatAdminRequired, PeerIdInvalid, ChannelInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LinkPreviewOptions

async def handle_force_subscribe(bot, message):
    if not Config.UPDATES_CHANNEL:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Updates channel not configured.\nPlease contact the admin.",
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )
        return 400

    try:
        invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return 400
    except (ChatAdminRequired, PeerIdInvalid, ChannelInvalid, KeyError, ValueError) as e:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Bot is not properly configured or missing access to the Updates Channel.\nPlease contact the admin!",
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )
        return 400

    try:
        user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), message.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=message.from_user.id,
                text="Sorry, you are banned from using this bot.",
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
            return 400
    except UserNotParticipant:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Please join the Updates Channel to use this bot!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Join Channel", url=invite_link.invite_link, style=enums.ButtonStyle.PRIMARY)],
                    [InlineKeyboardButton("Refresh", callback_data="refreshForceSub", style=enums.ButtonStyle.SUCCESS)]
                ]
            ),
        )
        return 400
    except Exception:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="An unexpected error occurred.\nPlease contact support.",
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )
        return 400
