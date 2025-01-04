# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | @NT_BOTS_SUPPORT | LISA-KOREA/UPLOADER-BOT-V4

# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/UPLOADER-BOT-V4



import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
from plugins.config import Config
from pyrogram import filters, Client, idle

logging.getLogger("pyrogram").setLevel(logging.WARNING)


if __name__ == "__main__" :

    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    plugins = dict(root="plugins")
    bot = Client(
        "URL UPLOADER BOT",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )


    user = Client(
        "User",
        session_string=Config.SESSION_STR,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH
    )

    bot.start()
    print("🎊 I AM ALIVE 🎊  • Support @NT_BOTS_SUPPORT")
  
    user.start()
    print("👤 User client is running!")
  
    try:
        Client.idle()
    except KeyboardInterrupt:
        print("Bot is shutting down...")
      
    user.stop()
    bot.stop()
     
