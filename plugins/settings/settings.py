

import asyncio
from pyrogram import types, errors, enums
from plugins.config import Config
from plugins.database.database import db

async def OpenSettings(m: "types.Message"):
    usr_id = m.chat.id
    user_data = await db.get_user_data(usr_id)
    if not user_data:
        await m.edit("Failed to fetch your data from the database!")
        return
    upload_as_doc = user_data.get("upload_as_doc", False)
    caption = user_data.get("caption", None)
    apply_caption = user_data.get("apply_caption", True)
    thumbnail = user_data.get("thumbnail", None)

    # Build the buttons for the settings
    buttons_markup = [
        [types.InlineKeyboardButton(f"ᴜᴘʟᴏᴀᴅ ᴀs {'🎥 ᴠɪᴅᴇᴏ' if upload_as_doc else '🗃️ Fɪʟᴇ'}",
                                    callback_data="triggerUploadMode")],
        [types.InlineKeyboardButton(f"{'ᴄʜᴀɴɢᴇ' if thumbnail else '🌃 sᴇᴛ'} ᴛʜᴜᴍʙɴᴀɪʟ",
                                    callback_data="setThumbnail")]
    ]

    if thumbnail:
        buttons_markup.append([types.InlineKeyboardButton("🌆 sʜᴏᴡ ᴛʜᴜᴍʙɴᴀɪʟ",
                                                          callback_data="showThumbnail")])

    # Add caption-related buttons
    buttons_markup.append([
        types.InlineKeyboardButton(f"ᴀᴘᴘʟʏ ᴄᴀᴘᴛɪᴏɴ: {'✅ ON' if apply_caption else '❌ OFF'}",
                                   callback_data="toggleApplyCaption"),
        types.InlineKeyboardButton("✏️ ᴇᴅɪᴛ ᴄᴀᴘᴛɪᴏɴ",
                                   callback_data="editCaption")
    ])

    buttons_markup.append([types.InlineKeyboardButton("♨️ ᴄʟᴏsᴇ",
                                                      callback_data="close")])

    try:
        await m.edit(
            text="**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ sᴇᴛᴜᴘ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs**",
            reply_markup=types.InlineKeyboardMarkup(buttons_markup),
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.MARKDOWN
        )
    except errors.MessageNotModified:
        pass
    except errors.FloodWait as e:
        await asyncio.sleep(e.x)
        await OpenSettings(m)
    except Exception as err:
        Config.LOGGER.getLogger(__name__).error(err)

