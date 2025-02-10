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
├📢 **Fʀᴀᴍᴇᴡᴏʀᴋ** : <a href=https://docs.pyrogram.org/>Pʏʀᴏꜰᴏʀᴋ 2.3.58</a>
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
    AFTER_SUCCESSFUL_UPLOAD_MSG = "OWNER : Lisa 💕\nFor the List of Telegram Bots"
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "**𝘛𝘏𝘈𝘕𝘒𝘚 𝘍𝘖𝘙 𝘜𝘚𝘐𝘕𝘎 𝘔𝘌** 🥰"
    #AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "PLEASE /DONATE TO KEEP THIS SERVICE ALIVE"
    NOT_AUTH_USER_TEXT = "Please /upgrade your subscription."
    NOT_AUTH_USER_TEXT_FILE_SIZE = "Detected File Size: {}. Free Users can only upload: {}\nPlease /upgrade your subscription."
    SAVED_CUSTOM_THUMB_NAIL = "**SAVED THUMBNAIL** ✅"
    DEL_ETED_CUSTOM_THUMB_NAIL = "**DELETED THUMBNAIL** ✅"
    FF_MPEG_DEL_ETED_CUSTOM_MEDIA = "✅ Media cleared succesfully."
    SAVED_RECVD_DOC_FILE = "Document Downloaded Successfully."
    CUSTOM_CAPTION_UL_FILE = " "
    NO_CUSTOM_THUMB_NAIL_FOUND = "ɴᴏ ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ"
    NO_VOID_FORMAT_FOUND = "ERROR... <code>{}</code>"
    FILE_NOT_FOUND = "Error, File not Found!!"
    USER_ADDED_TO_DB = "User <a href='tg://user?id={}'>{}</a> added to {} till {}."
    SOMETHING_WRONG = "<code>Something Wrong. Try again.</code>"
    REPLY_TO_DOC_GET_LINK = "Reply to a Telegram media to get High Speed Direct Download Link"
    REPLY_TO_DOC_FOR_C2V = "Reply to a Telegram media to convert"
    REPLY_TO_DOC_FOR_SCSS = "Reply to a Telegram media to get screenshots"
    REPLY_TO_DOC_FOR_RENAME_FILE = "Reply to a Telegram media to /ren with custom thumbnail support"
    AFTER_GET_LINK = " <b>File Name :</b> <code>{}</code>\n<b>File Size :</b> {}\n\n<b>⚡Link⚡ :</b> <code>{}</code>"
    AFTER_GET_DL_LINK = " <b>File Name :</b> <code>{}</code>\n<b>File Size :</b> {}\n\n<b>⚡Link⚡ :</b> <code>{}</code>\n\nValid for <b>14</b> days."
    #AFTER_GET_DL_LINK = " {} valid for 30 or more days.\n\n For the list of Telegram bots. "
    AFTER_GET_GOFILE_LINK = " <b>File Name :</b> <code>{}</code>\n<b>File Size :</b> {}\n<b>File MD5 Checksum :</b> <code>{}</code>\n\n<b>⚡Link⚡ :</b> <code>{}</code>\n\n Valid untill 10 days of inactivity"
    FF_MPEG_RO_BOT_RE_SURRECT_ED = """Syntax: /trim HH:MM:SS for screenshot of that specific time."""
    FF_MPEG_RO_BOT_STEP_TWO_TO_ONE = "First send /downloadmedia to any media so that it can be downloaded to my local. \nSend /storageinfo to know the media, that is currently downloaded."
    FF_MPEG_RO_BOT_STOR_AGE_INFO = "Video Duration: {}\nSend /clearffmpegmedia to delete this media, from my storage.\nSend /trim HH:MM:SS [HH:MM:SS] to cu[l]t a small photo / video, from the above media."
    FF_MPEG_RO_BOT_STOR_AGE_ALREADY_EXISTS = "A saved media already exists. Please send /storageinfo to know the current media details."
    USER_DELETED_FROM_DB = "User <a href='tg://user?id={}'>{}</a> deleted from DataBase."
    REPLY_TO_DOC_OR_LINK_FOR_RARX_SRT = "Reply to a Telegram media (MKV), to extract embedded streams"
    REPLY_TO_MEDIA_ALBUM_TO_GEN_THUMB = "Reply /generatecustomthumbnail to a media album, to generate custom thumbail"
    ERR_ONLY_TWO_MEDIA_IN_ALBUM = "Media Album should contain only two photos. Please re-send the media album, and then try again, or send only two photos in an album."
    INVALID_UPLOAD_BOT_URL_FORMAT = "URL format is incorrect. make sure your url starts with either http:// or https://. You can set custom file name using the format link | file_name.extension"
    ABUSIVE_USERS = "You are not allowed to use this bot. If you think this is a mistake, please check /me to remove this restriction."
    FF_MPEG_RO_BOT_AD_VER_TISE_MENT = "Join : @NT_BOT_CHANNEL \n For the list of Telegram bots. "
    EXTRACT_ZIP_INTRO_ONE = "Send a compressed file first, Then reply /unzip command to the file."
    EXTRACT_ZIP_INTRO_THREE = "Analyzing received file. ⚠️ This might take some time. Please be patient. "
    UNZIP_SUPPORTED_EXTENSIONS = ("zip", "rar")
    EXTRACT_ZIP_ERRS_OCCURED = "Sorry. Errors occurred while processing compressed file. Please check everything again twice, and if the issue persists, report this to <a href='https://telegram.dog/ThankTelegram'>@SpEcHlDe</a>"
    EXTRACT_ZIP_STEP_TWO = """**This is not a rename bot** 🤭\n\nUse @FastRenameBot 4gb support"""
    CANCEL_STR = "Process Cancelled"
    ZIP_UPLOADED_STR = "Uploaded {} files in {} seconds"
    FREE_USER_LIMIT_Q_SZE = """Pʟᴇᴀsᴇ ᴡᴀɪᴛ {} Sᴇᴄᴏɴᴅs"""
    SLOW_URL_DECED = "Gosh that seems to be a very slow URL. Since you were screwing my home, I am in no mood to download this file. Meanwhile, why don't you try this:==> https://shrtz.me/PtsVnf6 and get me a fast URL so that I can upload to Telegram, without me slowing down for other users."
    FORCE_SUBSCRIBE_TEXT = "<code>Sorry Dear You Must Join My Updates Channel for using me 😌😉....</code>"
    BANNED_USER_TEXT = "<code>You are Banned!</code>"
    CHECK_LINK = "⚡️"

    ADD_CAPTION_HELP = """Select an uploaded file/video or forward me <b>Any Telegram File</b> and just write the text you want to be on the file <b>as a reply to the file</b> and the text you wrote will be attached as the caption! 🤩
    
Example: <a href='https://te.legra.ph/file/ecf5297246c5fb574d1a0.jpg'>See This!</a> 👇"""
