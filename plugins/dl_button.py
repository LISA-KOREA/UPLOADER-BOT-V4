# @Shrimadhav Uk | @LISA_FAN_LK
import logging
import asyncio
import aiohttp
import json
import math
import os
import shutil
import time
from datetime import datetime

from plugins.config import Config
from plugins.script import Translation
from plugins.thumbnail import *
from plugins.database.database import db
from plugins.functions.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from pyrogram import enums

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


async def ddl_call_back(bot, update):
    logger.info(update)
    cb_data = update.data
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("=")

    youtube_dl_url = update.message.reply_to_message.text
    custom_file_name = os.path.basename(youtube_dl_url)

    if "|" in youtube_dl_url:
        url_parts = youtube_dl_url.split("|")
        if len(url_parts) == 2:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
        else:
            for entity in update.message.reply_to_message.entities:
                if entity.type == "text_link":
                    youtube_dl_url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    youtube_dl_url = youtube_dl_url[o:o + l]

        if youtube_dl_url is not None:
            youtube_dl_url = youtube_dl_url.strip()
        if custom_file_name is not None:
            custom_file_name = custom_file_name.strip()

        logger.info(youtube_dl_url)
        logger.info(custom_file_name)
    else:
        for entity in update.message.reply_to_message.entities:
            if entity.type == "text_link":
                youtube_dl_url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                youtube_dl_url = youtube_dl_url[o:o + l]

    description = Translation.CUSTOM_CAPTION_UL_FILE
    start = datetime.now()

    await update.message.edit_caption(
        caption=Translation.DOWNLOAD_START,
        parse_mode=enums.ParseMode.HTML
    )

    tmp_directory_for_each_user = os.path.join(
        Config.DOWNLOAD_LOCATION, str(update.from_user.id)
    )
    os.makedirs(tmp_directory_for_each_user, exist_ok=True)

    download_directory = os.path.join(tmp_directory_for_each_user, custom_file_name)

    async with aiohttp.ClientSession() as session:
        c_time = time.time()
        try:
            await download_coroutine(
                bot,
                session,
                youtube_dl_url,
                download_directory,
                update.message.chat.id,
                update.message.id,
                c_time
            )
        except asyncio.TimeoutError:
            await bot.edit_message_text(
                text=Translation.SLOW_URL_DECED,
                chat_id=update.message.chat.id,
                message_id=update.message.id
            )
            return False
        except Exception as e:
            logger.error(f"Download failed: {e}")
            await update.message.edit_caption(
                caption=f"Download Error: {e}",
                parse_mode=enums.ParseMode.HTML
            )
            return False

    if not os.path.exists(download_directory):
        possible_mkv = os.path.splitext(download_directory)[0] + ".mkv"
        if os.path.exists(possible_mkv):
            download_directory = possible_mkv
        else:
            await update.message.edit_caption(
                caption=Translation.NO_VOID_FORMAT_FOUND.format("Incorrect Link"),
                parse_mode=enums.ParseMode.HTML
            )
            return False

    end_one = datetime.now()
    time_taken_for_download = (end_one - start).seconds

    try:
        file_size = os.stat(download_directory).st_size
    except Exception as e:
        logger.error(f"Cannot get file size: {e}")
        await update.message.edit_caption(
            caption=Translation.NO_VOID_FORMAT_FOUND.format("File not found after download"),
            parse_mode=enums.ParseMode.HTML
        )
        return False

    if file_size > Config.TG_MAX_FILE_SIZE:
        await update.message.edit_caption(
            caption=Translation.RCHD_TG_API_LIMIT,
            parse_mode=enums.ParseMode.HTML
        )
        try:
            os.remove(download_directory)
        except Exception:
            pass
        return False

    await update.message.edit_caption(
        caption=Translation.UPLOAD_START,
        parse_mode=enums.ParseMode.HTML
    )

    start_time = time.time()
    thumbnail = None

    try:
        if tg_send_type == "audio":
            duration = await Mdata03(download_directory)
            thumbnail = await Gthumb01(bot, update)
            await update.message.reply_audio(
                audio=download_directory,
                caption=description,
                parse_mode=enums.ParseMode.HTML,
                duration=duration,
                thumb=thumbnail,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START,
                    update.message,
                    start_time
                )
            )

        elif tg_send_type == "vm":
            width, duration = await Mdata02(download_directory)
            thumbnail = await Gthumb02(bot, update, duration, download_directory)
            await update.message.reply_video_note(
                video_note=download_directory,
                duration=duration,
                length=width,
                thumb=thumbnail,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START,
                    update.message,
                    start_time
                )
            )

        else:
            if (await db.get_upload_as_doc(update.from_user.id)) is False:
                thumbnail = await Gthumb01(bot, update)
                await update.message.reply_document(
                    document=download_directory,
                    thumb=thumbnail,
                    caption=description,
                    parse_mode=enums.ParseMode.HTML,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        start_time
                    )
                )
            else:
                width, height, duration = await Mdata01(download_directory)
                thumbnail = await Gthumb02(bot, update, duration, download_directory)
                await update.message.reply_video(
                    video=download_directory,
                    caption=description,
                    duration=duration,
                    width=width,
                    height=height,
                    supports_streaming=True,
                    parse_mode=enums.ParseMode.HTML,
                    thumb=thumbnail,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        start_time
                    )
                )

        logger.info("✅ Upload completed successfully")

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        await update.message.edit_caption(
            caption=f"Upload Error: {e}",
            parse_mode=enums.ParseMode.HTML
        )

    end_two = datetime.now()
    time_taken_for_upload = (end_two - end_one).seconds

    try:
        if os.path.exists(download_directory):
            os.remove(download_directory)
    except Exception as e:
        logger.error(f"Error removing downloaded file: {e}")

    if thumbnail and os.path.exists(thumbnail):
        try:
            os.remove(thumbnail)
        except Exception as e:
            logger.error(f"Error removing thumbnail: {e}")

    await update.message.edit_caption(
        caption=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(
            time_taken_for_download, time_taken_for_upload
        ),
        parse_mode=enums.ParseMode.HTML
    )


async def download_coroutine(bot, session, url, file_name, chat_id, message_id, start):
    downloaded = 0
    display_message = ""

    async with session.get(url, timeout=Config.PROCESS_MAX_TIMEOUT) as response:
        content_length = response.headers.get("Content-Length")
        if content_length is None:
            total_length = 0
        else:
            total_length = int(content_length)
        content_type = response.headers.get("Content-Type", "")
        if "text" in content_type and total_length < 500:
            await response.release()
            return

        await bot.edit_message_text(
            chat_id,
            message_id,
            text="""Initiating Download
URL: {}
File Size: {}""".format(url, humanbytes(total_length) if total_length else "Unknown")
        )

        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(Config.CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += len(chunk)      

                now = time.time()
                diff = now - start

                if total_length > 0 and (round(diff % 5.00) == 0 or downloaded >= total_length):
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff if diff > 0 else 0
                    elapsed_time = round(diff) * 1000
                    time_to_completion = round((total_length - downloaded) / speed) * 1000 if speed > 0 else 0
                    estimated_total_time = elapsed_time + time_to_completion

                    try:
                        current_message = """**Download Status**
URL: {}
File Size: {}
Downloaded: {}
ETA: {}""".format(
                            url,
                            humanbytes(total_length),
                            humanbytes(downloaded),
                            TimeFormatter(estimated_total_time)
                        )
                        if current_message != display_message:
                            await bot.edit_message_text(
                                chat_id,
                                message_id,
                                text=current_message
                            )
                            display_message = current_message
                    except Exception as e:
                        logger.info(str(e))

        await response.release()
