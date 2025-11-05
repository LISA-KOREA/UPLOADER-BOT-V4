import os
import logging

logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler()
    ],
    level=logging.INFO
)

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7507976245:AAHYGdOX3__OTEzRMtLCs49vh4F_ZrdBfvU")
    API_ID = int(os.environ.get("API_ID", "27079727"))
    API_HASH = os.environ.get("API_HASH", "c9beff017aa24d112b259159057936e2")

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
    DEF_WATER_MARK_FILE = "@UploaderXNTBot"

    BANNED_USERS = set(
        int(x) for x in os.environ.get("BANNED_USERS", "").split() if x.strip()
    )

    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "mongodb+srv://root:Bhadasar1#@cluster0.uoxgl1h.mongodb.net/?appName=Cluster0"
    )

    LOG_CHANNEL_ENV = os.environ.get("LOG_CHANNEL")
    LOG_CHANNEL = int(LOG_CHANNEL_ENV) if LOG_CHANNEL_ENV else None
    OWNER_ID = int(os.environ.get("OWNER_ID", "1071594702"))

    UPDATES_CHANNEL_ENV = os.environ.get("UPDATES_CHANNEL")
    UPDATES_CHANNEL = int(UPDATES_CHANNEL_ENV) if UPDATES_CHANNEL_ENV else None

    TG_MIN_FILE_SIZE = 2194304000
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "Reezexbot")

    TRUE_OR_FALSE = os.environ.get("TRUE_OR_FALSE", "").lower() == "true"
    SHORT_DOMAIN = os.environ.get("SHORT_DOMAIN", "")
    SHORT_API = os.environ.get("SHORT_API", "")

    VERIFICATION = os.environ.get("VERIFICATION", "")
    ADL_BOT_RQ = {}
