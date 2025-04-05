from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Translation(object):

    START_TEXT = """👋 Hᴇʟʟᴏ {} 

ⵊ Aᴍ Tᴇʟᴇɢʀᴀᴍ URL Uᴘʟᴏᴀᴅᴇʀ Bᴏᴛ.

**Sᴇɴᴅ ᴍᴇ ᴀ ᴅɪʀᴇᴄᴛ ʟɪɴᴋ ᴀɴᴅ ɪ ᴡɪʟʟ ᴜᴘʟᴏᴀᴅ ɪᴛ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ᴀs ᴀ ꜰɪʟᴇ/ᴠɪᴅᴇᴏ**

Usᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ

"""
    

    HELP_TEXT = """
**Hᴏᴡ Tᴏ Usᴇ Tʜɪs Bᴏᴛ** 🤔
   
𖣔 Fɪʀsᴛ ɢᴏ ᴛᴏ ᴛʜᴇ /settings ᴀɴᴅ ᴄʜᴀɴɢᴇ ᴛʜᴇ ʙᴏᴛ ʙᴇʜᴀᴠɪᴏʀ ᴀs ʏᴏᴜʀ ᴄʜᴏɪᴄᴇ.

𖣔 Sᴇɴᴅ ᴍᴇ ᴛʜᴇ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ ᴛᴏ sᴀᴠᴇ ɪᴛ ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ.

𖣔 **Sᴇɴᴅ ᴜʀʟ | Nᴇᴡ ɴᴀᴍᴇ.ᴍᴋᴠ**

𖣔 Sᴇʟᴇᴄᴛ ᴛʜᴇ ᴅᴇsɪʀᴇᴅ ᴏᴘᴛɪᴏɴ.

𖣔 Usᴇ `/caption` ᴛᴏ sᴇᴛ ᴄᴀᴘᴛɪᴏɴ ᴀs Rᴇᴘʟʏ ᴛᴏ ᴍᴇᴅɪᴀ

"""
    
    ABOUT_TEXT ="""
╭───────────⍟
├📛 **Mʏ Nᴀᴍᴇ** : URL Uᴘʟᴏᴀᴅᴇʀ Bᴏᴛ
├📢 **Fʀᴀᴍᴇᴡᴏʀᴋ** : <a href=https://docs.pyrogram.org/>Pʏʀᴏꜰᴏʀᴋ 2.3.60</a>
├💮 **Lᴀɴɢᴜᴀɢᴇ** : <a href=https://www.python.org>Pʏᴛʜᴏɴ 3.13.2</a>
├💾 **Dᴀᴛᴀʙᴀsᴇ** : <a href=https://cloud.mongodb.com>MᴏɴɢᴏDB</a>
├🚨 **Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ** : <a href=https://t.me/NT_BOTS_SUPPORT>Nᴛ Sᴜᴘᴘᴏʀᴛ</a>
├🥏 **Cʜᴀɴɴᴇʟ** : <a href=https://t.me/NT_BOT_CHANNEL>Nᴛ Bᴏᴛ Cʜᴀɴɴᴇʟ</a>
├👨‍💻 **Cʀᴇᴀᴛᴇʀ** :  @NT_BOT_CHANNEL
╰───────────────⍟
"""


    PROGRESS = """
┣📦 Pʀᴏɢʀᴇꜱꜱ : {0}%
┣ ✅ Dᴏɴᴇ : {1}
┣ 📁 Tᴏᴛᴀʟ : {2}
┣ 🚀 Sᴘᴇᴇᴅ : {3}/s
┣ 🕒 Tɪᴍᴇ : {4}
┗━━━━━━━━━━━━━━━━━━━━
"""

    PROGRES = """
`{}`\n{}"""


    INFO_TEXT = """
╭──────────────〄
├📛 **Fɪʀsᴛ Nᴀᴍᴇ :** <b>{}</b>
├📛 **Sᴇᴄᴏɴᴅ Nᴀᴍᴇ :** <b>{}</b>
├👤 **Usᴇʀɴᴀᴍᴇ :** <b>@{}</b>
├🆔 **Tᴇʟᴇɢʀᴀᴍ ⵊᴅ :** <code>{}</code>
├🖇️ **Pʀᴏꜰɪʟᴇ Lɪɴᴋ :** <b>{}</b>
├📡 **Dᴄ :** <b>{}</b>
├💮 **Lᴀɴɢᴜᴀɢᴇ:** <b>{}</b>
├💫 **Sᴛᴀᴛᴜs :** <b>{}</b>
╰──────────────────〄
"""


    START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🛠️ SETTINGS', callback_data='OpenSettings')
        ],[
        InlineKeyboardButton('🤝 HELP', callback_data='help'),
        InlineKeyboardButton('🎯 ABOUT', callback_data='about')
        ],[
        InlineKeyboardButton('⛔ CLOSE', callback_data='close')
        ]]
    )
    HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🛠️ SETTINGS', callback_data='OpenSettings')
        ],[
        InlineKeyboardButton('🔙 BACK', callback_data='home'),
        InlineKeyboardButton('🎯 ABOUT', callback_data='about')
        ],[
        InlineKeyboardButton('⛔ CLOSE', callback_data='close')
        ]]
    )
    ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🛠️ SETTINGS', callback_data='OpenSettings')
        ],[
        InlineKeyboardButton('🔙 BACK', callback_data='home'),
        InlineKeyboardButton('🤝 HELP', callback_data='help')
        ],[
        InlineKeyboardButton('⛔ CLOSE', callback_data='close')
        ]]
    )
    PLANS_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🎯 ABOUT', callback_data='about')
        ],[
        InlineKeyboardButton('🔙 BACK', callback_data='home'),
        InlineKeyboardButton('🤝 HELP', callback_data='help')
        ],[
        InlineKeyboardButton('⛔ CLOSE', callback_data='close')
        ]]
   )
    BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⛔ Close', callback_data='close')
        ]]
    )
    INCORRECT_REQUEST = """Eʀʀᴏʀ"""
    DOWNLOAD_FAILED = "🔴 Eʀʀᴏʀ 🔴"
    TEXT = "Sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ"
    IFLONG_FILE_NAME = " Only 64 characters can be named . "
    RENAME_403_ERR = "Sorry. You are not permitted to rename this file."
    ABS_TEXT = " Please don't be selfish."
    FORMAT_SELECTION = "<b>Sᴇʟᴇᴄᴛ Yᴏᴜʀ Fᴏʀᴍᴀᴛ 👇</b>\n"
    SET_CUSTOM_USERNAME_PASSWORD = """<b>🎥 Vɪᴅᴇᴏ = Uᴘʟᴏᴀᴅ As Sᴛʀᴇᴀᴍʙʟᴇ</b>\n\n<b>📂 Fɪʟᴇ = Uᴘʟᴏᴀᴅ As Fɪʟᴇ</b>\n\n<b>👮‍♂ Pᴏᴡᴇʀᴇᴅ Bʏ :</b> @NT_BOT_CHANNEL"""
    NOYES_URL = "@robot URL detected. Please use https://shrtz.me/PtsVnf6 and get me a fast URL so that I can upload to Telegram, without me slowing down for other users."
    DOWNLOAD_START = "📥 Downloading... 📥\n\nFile Name: {}"
    UPLOAD_START = "📤 Uploading... 📤"
    RCHD_BOT_API_LIMIT = "size greater than maximum allowed size (50MB). Neverthless, trying to upload."
    RCHD_TG_API_LIMIT = "Downloaded in {} seconds.\nDetected File Size: {}\nSorry. But, I cannot upload files greater than 2000MB due to Telegram API limitations."
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "**𝘛𝘏𝘈𝘕𝘒𝘚 𝘍𝘖𝘙 𝘜𝘚𝘐𝘕𝘎 𝘔𝘌** 🥰"
    SAVED_CUSTOM_THUMB_NAIL = "**SAVED THUMBNAIL** ✅"
    DEL_ETED_CUSTOM_THUMB_NAIL = "**DELETED THUMBNAIL** ✅"
    FF_MPEG_DEL_ETED_CUSTOM_MEDIA = "✅ Media cleared succesfully."
    CUSTOM_CAPTION_UL_FILE = " "
    NO_CUSTOM_THUMB_NAIL_FOUND = "ɴᴏ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ"
    NO_VOID_FORMAT_FOUND = "ERROR... <code>{}</code>"
    FILE_NOT_FOUND = "Error, File not Found!!"
    FF_MPEG_RO_BOT_AD_VER_TISE_MENT = "Join : @NT_BOT_CHANNEL \n For the list of Telegram bots. "
    ADD_CAPTION_HELP = """Select an uploaded file/video or forward me <b>Any Telegram File</b> and just write the text you want to be on the file <b>as a reply to the file</b> and the text you wrote will be attached as the caption! 🤩
    
Example: <a href='https://te.legra.ph/file/ecf5297246c5fb574d1a0.jpg'>See This!</a> 👇"""
