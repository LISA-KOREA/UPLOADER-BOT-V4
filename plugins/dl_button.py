# @Shrimadhav Uk | @LISA_FAN_LK


import logging
import asyncio
import aiohttp
import os
import time
from datetime import datetime
from plugins.config import Config
from plugins.script import Translation
from plugins.thumbnail import *
from plugins.database.database import db
from plugins.functions.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from pyrogram import enums 

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Function to split a file into chunks
def split_file(file_path, chunk_size=Config.TG_MAX_FILE_SIZE):
    file_size = os.stat(file_path).st_size
    if file_size <= chunk_size:
        return [file_path]
    
    chunk_paths = []
    with open(file_path, 'rb') as f:
        part_number = 1
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            chunk_filename = f"{file_path}_part_{part_number}"
            with open(chunk_filename, 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunk_paths.append(chunk_filename)
            part_number += 1
    return chunk_paths

async def ddl_call_back(bot, update):
    logger.info(update)
    cb_data = update.data
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("=")
    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    youtube_dl_url = update.message.reply_to_message.text
    custom_file_name = os.path.basename(youtube_dl_url)

    # Handle special URL format
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

    # Cleanup URL and file name
    if youtube_dl_url is not None:
        youtube_dl_url = youtube_dl_url.strip()
    if custom_file_name is not None:
        custom_file_name = custom_file_name.strip()

    # Description and progress info
    description = Translation.CUSTOM_CAPTION_UL_FILE
    start = datetime.now()
    await update.message.edit_caption(caption=Translation.DOWNLOAD_START, parse_mode=enums.ParseMode.HTML)

    # Prepare directory for user download
    tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)

    # Set download path
    download_directory = tmp_directory_for_each_user + "/" + custom_file_name
    command_to_exec = []

    # Download the file
    async with aiohttp.ClientSession() as session:
        c_time = time.time()
        try:
            await download_coroutine(bot, session, youtube_dl_url, download_directory, update.message.chat.id, update.message.id, c_time)
        except asyncio.TimeoutError:
            await bot.edit_message_text(text=Translation.SLOW_URL_DECED, chat_id=update.message.chat.id, message_id=update.message.id)
            return False

    # After successful download
    if os.path.exists(download_directory):
        end_one = datetime.now()
        await update.message.edit_caption(caption=Translation.UPLOAD_START, parse_mode=enums.ParseMode.HTML)

        # Check file size
        file_size = Config.TG_MAX_FILE_SIZE + 1
        try:
            file_size = os.stat(download_directory).st_size
        except FileNotFoundError as exc:
            download_directory = os.path.splitext(download_directory)[0] + "." + "mkv"
            file_size = os.stat(download_directory).st_size

        # Split the file if it's too large
        if file_size > Config.TG_MAX_FILE_SIZE:
            chunk_files = split_file(download_directory)
            for chunk in chunk_files:
                # Upload each chunk as a document
                await update.message.reply_document(
                    document=chunk,
                    caption=description,
                    parse_mode=enums.ParseMode.HTML,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, update.message, time.time())
                )
                # Clean up after sending each chunk
                os.remove(chunk)
        else:
            # If file size is small enough, just send the file
            start_time = time.time()
            if (await db.get_upload_as_doc(update.from_user.id)) is False:
                thumbnail = await Gthumb01(bot, update)
                await update.message.reply_document(
                    document=download_directory,
                    thumb=thumbnail,
                    caption=description,
                    parse_mode=enums.ParseMode.HTML,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, update.message, start_time)
                )
            else:
                width, height, duration = await Mdata01(download_directory)
                thumb_image_path = await Gthumb02(bot, update, duration, download_directory)
                await update.message.reply_video(
                    video=download_directory,
                    caption=description,
                    duration=duration,
                    width=width,
                    height=height,
                    supports_streaming=True,
                    parse_mode=enums.ParseMode.HTML,
                    thumb=thumb_image_path,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, update.message, start_time)
                )
            # Handle audio files
            if tg_send_type == "audio":
                duration = await Mdata03(download_directory)
                thumbnail = await Gthumb01(bot, update)
                await update.message.reply_audio(
                    audio=download_directory,
                    caption=description,
                    duration=duration,
                    thumb=thumbnail,
                    parse_mode=enums.ParseMode.HTML,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, update.message, start_time)
                )
            # Handle video notes
            elif tg_send_type == "vm":
                width, duration = await Mdata02(download_directory)
                thumbnail = await Gthumb02(bot, update, duration, download_directory)
                await update.message.reply_video_note(
                    video_note=download_directory,
                    duration=duration,
                    length=width,
                    thumb=thumbnail,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, update.message, start_time)
                )
            else:
                logger.info("Unknown file type")
            end_two = datetime.now()

            # Clean up after upload
            try:
                os.remove(download_directory)
                os.remove(thumb_image_path)
            except Exception as e:
                logger.error("Error cleaning up files: ", e)

            time_taken_for_download = (end_one - start).seconds
            time_taken_for_upload = (end_two - end_one).seconds
            await update.message.edit_caption(
                caption=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload),
                parse_mode=enums.ParseMode.HTML
            )
    else:
        await update.message.edit_caption(caption=Translation.NO_VOID_FORMAT_FOUND.format("Incorrect Link"), parse_mode=enums.ParseMode.HTML)


# Download function to handle the file download from URL
async def download_coroutine(bot, session, url, file_name, chat_id, message_id, start):
    downloaded = 0
    display_message = ""
    async with session.get(url, timeout=Config.PROCESS_MAX_TIMEOUT) as response:
        total_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        
        if "text" in content_type and total_length < 500:
            return await response.release()

        # Update download status
        await bot.edit_message_text(
            chat_id,
            message_id,
            text="""Initiating Download
            
**🔗 Uʀʟ :** `{}`

**🗂️ Sɪᴢᴇ :** {}""".format(url, humanbytes(total_length))
        )
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(Config.CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += Config.CHUNK_SIZE
                now = time.time()
                diff = now - start
                if round(diff % 5.00) == 0 or downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = round((total_length - downloaded) / speed) * 1000
                    estimated_total_time = elapsed_time + time_to_completion
                    try:
                        current_message = """**Download Status**
**🔗 Uʀʟ :** `{}`

**🗂️ Sɪᴢᴇ :** {}

**✅ Dᴏɴᴇ :** {}

**⏱️ Eᴛᴀ :** {}""".format(
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
                        pass
        return await response.release()
