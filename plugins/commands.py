import random
import os
import time
import psutil
import shutil
import string
import asyncio
from pyrogram import Client, filters
from asyncio import TimeoutError
from pyrogram.types import Message 
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from plugins.config import Config
from plugins.script import Translation
from pyrogram import Client, filters
from plugins.database.add import AddUser
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.database.database import db
from plugins.functions.forcesub import handle_force_subscribe
from plugins.settings.settings import OpenSettings
from plugins.config import *
from plugins.functions.verify import verify_user, check_token
from pyrogram import types, errors




@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if Config.UPDATES_CHANNEL is not None:
        fsub = await handle_force_subscribe(bot, update)
        if fsub == 400:
            return
    if len(update.command) != 2:
        await AddUser(bot, update)
        await update.reply_text(
            text=Translation.START_TEXT.format(update.from_user.mention),
            reply_markup=Translation.START_BUTTONS,
        )
        return
    data = update.command[1]
    if data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        if str(update.from_user.id) != str(userid):
            return await update.reply_text(
                text="<b>Exᴘɪʀᴇᴅ Lɪɴᴋ Oʀ ⵊɴᴠᴀʟɪᴅ Lɪɴᴋ !</b>",
                protect_content=True
            )
        is_valid = await check_token(bot, userid, token)
        if is_valid == True:
            await update.reply_text(
                text=f"<b>Hᴇʏ {update.from_user.mention} 👋,\nʏᴏᴜ Aʀᴇ Sᴜᴄᴄᴇssғᴜʟʟʏ Vᴇʀɪғɪᴇᴅ !\n\nNᴏᴡ Yᴏᴜ Uᴘʟᴏᴀᴅ Fɪʟᴇs Aɴᴅ Vɪᴅᴇᴏs Tɪʟʟ Tᴏᴅᴀʏ Mɪᴅɴɪɢʜᴛ.</b>",
                protect_content=True
            )
            await verify_user(bot, userid, token)
        else:
            return await update.reply_text(
                text="<b>Exᴘɪʀᴇᴅ Lɪɴᴋ Oʀ ⵊɴᴠᴀʟɪᴅ Lɪɴᴋ !</b>",
                protect_content=True
            )



@Client.on_message(filters.command("help", [".", "/"]) & filters.private)
async def help_bot(_, m: Message):
    await AddUser(_, m)
    return await m.reply_text(
        Translation.HELP_TEXT,
        reply_markup=Translation.HELP_BUTTONS,
        disable_web_page_preview=True,
    )

@Client.on_message(filters.command("about", [".", "/"]) & filters.private)
async def aboutme(_, m: Message):
    await AddUser(_, m)
    return await m.reply_text(
        Translation.ABOUT_TEXT,
        reply_markup=Translation.ABOUT_BUTTONS,
        disable_web_page_preview=True,
    )

@Client.on_message(filters.private & filters.reply & filters.text)
async def edit_caption(bot, update):
    await AddUser(bot, update)
    try:
        await bot.send_cached_media(
            chat_id=update.chat.id,
            file_id=update.reply_to_message.video.file_id,
            caption=update.text
        )
    except:
        try:
            await bot.send_cached_media(
                chat_id=update.chat.id,
                file_id=update.reply_to_message.document.file_id,
                caption=update.text
            )
        except:
            pass


@Client.on_message(filters.private & filters.command(["caption"], [".", "/"]))
async def add_caption_help(bot, update):
    await AddUser(bot, update)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ADD_CAPTION_HELP,
        reply_markup=Translation.BUTTONS,
    )


@Client.on_callback_query(filters.regex('^cancel_download\+'))
async def cancel_cb(c, m):
    await m.answer()
    await m.message.edit(text="Trying to Cancel")
    id = m.data.split("+", 1)[1]
    if id not in Config.DOWNLOAD_LOCATION:
        await m.message.edit("This process already cancelled reason may be bot restarted")
        return
    Config.DOWNLOAD_LOCATION.remove(id)


@Client.on_message(filters.private & filters.command("info", [".", "/"]))
async def info_handler(bot, update):
    if update.from_user.last_name:
        last_name = update.from_user.last_name
    else:
        last_name = "None"
    await update.reply_text(  
        text=Translation.INFO_TEXT.format(update.from_user.first_name, last_name, update.from_user.username, update.from_user.id, update.from_user.mention, update.from_user.dc_id, update.from_user.language_code, update.from_user.status), 
        reply_markup=Translation.BUTTONS,           
        disable_web_page_preview=True
    )


@Client.on_message(filters.command("warn"))
async def warn(c, m):
    if m.from_user.id in Config.OWNER_II:
        if len(m.command) >= 3:
            try:
                user_id = m.text.split(' ', 2)[1]
                reason = m.text.split(' ', 2)[2]
                await m.reply_text("User Notfied Sucessfully")
                await c.send_message(chat_id=int(user_id), text=reason)
            except:
                 await m.reply_text("User Not Notfied Sucessfully 😔")
    else:
        await m.reply_text(text="You Are Not Admin 😡", quote=True)


