import asyncio
from pyrogram import types, errors, filters
from pyrogram.types import Message
from plugins.config import Config
from plugins.database.database import db
from plugins.database.add import AddUser
from pyrogram import Client

async def OpenSettings(m: "types.Message"):
    usr_id = m.chat.id
    user_data = await db.get_user_data(usr_id)
    if not user_data:
        await m.edit("Failed to fetch your data from database!")
        return
    upload_as_doc = user_data.get("upload_as_doc", False)
    thumbnail = user_data.get("thumbnail", None)
    buttons_markup = [
        [types.InlineKeyboardButton(f" {'📹 VIDEO' if upload_as_doc else '📁 DOCUMENT'}",
                                    callback_data="triggerUploadMode")],
        [types.InlineKeyboardButton(f"{'🏞 CHANGE' if thumbnail else '🏞 SET'} THUMBNAIL",
                                    callback_data="setThumbnail")]
    ]
    if thumbnail:
        buttons_markup.append([types.InlineKeyboardButton("🏞 SHOW THUMBNAIL",
                                                          callback_data="showThumbnail")])
    buttons_markup.append([types.InlineKeyboardButton("🔙 BACK", 
                                                      callback_data="home")])

    try:
        await m.edit(
            text="**CURRENT SETTINGS 👇**",
            reply_markup=types.InlineKeyboardMarkup(buttons_markup),
            disable_web_page_preview=True,
        )
    except errors.MessageNotModified: pass
    except errors.FloodWait as e:
        await asyncio.sleep(e.x)
        await show_settings(m)
    except Exception as err:
        Config.LOGGER.getLogger(__name__).error(err)



@Client.on_message(filters.private & filters.command("settings"))
async def settings_handler(bot: Client, m: Message):
    await AddUser(bot, m)
    editable = await m.reply_text("**Checking...**", quote=True)
    await OpenSettings(editable)
