import os
from os import environ, getenv
import logging

logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO
)

class Config(object):
    
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8263561989:AAFerAlqlvUAE3Ks_pOwnV5otP9U-XdIr6E")
    API_ID = int(os.environ.get("API_ID", "35691135")
    API_HASH = os.environ.get("API_HASH", "5d1ea759af097ea5ae4b61dcbe82ff07")
    
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    MAX_FILE_SIZE = 2194304000
    TG_MAX_FILE_SIZE = 2194304000
    FREE_USER_MAX_FILE_SIZE = 2194304000
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))
    DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "https://placehold.it/90x90")
    HTTP_PROXY = os.environ.get("HTTP_PROXY", "")
    
    OUO_IO_API_KEY = ""
    MAX_MESSAGE_LENGTH = 4096
    PROCESS_MAX_TIMEOUT = 3600
    DEF_WATER_MARK_FILE = "@UploaderUGXBot"

    ADMIN = set(
        int(x) for x in environ.get("ADMIN", "8472871705 5890983034 6774514204").split()
        if x.isdigit()
    )

    BANNED_USERS = set(
        int(x) for x in environ.get("BANNED_USERS", "").split()
        if x.isdigit()
    )

    DATABASE_URL = os.environ.get("DATABASE_URL", "")

    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))
    LOGGER = logging
    OWNER_ID = int(os.environ.get("OWNER_ID", "5890983034"))
    SESSION_NAME = "UploaderXNTBot"
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "-1002906696187")

    TG_MIN_FILE_SIZE = 2194304000
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")
    ADL_BOT_RQ = {}

    # Set False off else True
    TRUE_OR_FALSE = os.environ.get("TRUE_OR_FALSE", "").lower() == "true"

    # Shortlink settings
    SHORT_DOMAIN = environ.get("SHORT_DOMAIN", "")
    SHORT_API = environ.get("SHORT_API", "")

    # Verification video link
    VERIFICATION = os.environ.get("VERIFICATION", "")

    
