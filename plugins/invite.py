from pyrogram import Client, filters
from plugins.config import Config
from pyrogram.types import ( InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
@Client.on_message(filters.private & filters.command(["invite"]))
async def refer(client,message):
    reply_markup = InlineKeyboardMarkup(
       		[ [ InlineKeyboardButton("📡 Sʜᴀʀᴇ Yᴏᴜʀ Lɪɴᴋ" ,url=f"https://t.me/share/url?url=https://t.me/{Config.BOT_USERNAME}?start={message.from_user.id}") ]   ])
    await message.reply_text(f"**INVITE YOUR FRIENDS**",reply_markup=reply_markup,)

