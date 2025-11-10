# Â©ï¸ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | TG-SORRY
# Simplified version with 1080p and Best Available options only

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import requests, urllib.parse, filetype, os, time, shutil, tldextract, asyncio, json, math
from PIL import Image
from plugins.config import Config
from plugins.script import Translation
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import filters
import os
import time
import random
from pyrogram import enums
from pyrogram import Client
from plugins.functions.verify import verify_user, check_token, check_verification, get_token
from plugins.functions.forcesub import handle_force_subscribe
from plugins.functions.display_progress import humanbytes
from plugins.functions.help_uploadbot import DownLoadFile
from plugins.functions.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from plugins.functions.ran_text import random_char
from plugins.database.database import db
from plugins.database.add import AddUser
from pyrogram.types import Thumbnail
import yt_dlp
import re

cookies_file = 'cookies.txt'

def ensure_cookies_file():
    """
    Create a valid Netscape format cookies file if it doesn't exist.
    Returns True if cookies file is valid/created, False otherwise.
    """
    if not os.path.exists(cookies_file):
        logger.info(f"Creating new cookies file: {cookies_file}")
        try:
            with open(cookies_file, 'w') as f:
                f.write("# Netscape HTTP Cookie File\n")
                f.write("# This is a generated file! Do not edit.\n\n")
            return True
        except Exception as e:
            logger.error(f"Failed to create cookies file: {e}")
            return False
    
    # Validate existing cookies file
    try:
        with open(cookies_file, 'r') as f:
            first_line = f.readline().strip()
            if not first_line.startswith("# Netscape HTTP Cookie File"):
                logger.warning("Invalid cookies file format, recreating...")
                with open(cookies_file, 'w') as f:
                    f.write("# Netscape HTTP Cookie File\n")
                    f.write("# This is a generated file! Do not edit.\n\n")
        return True
    except Exception as e:
        logger.error(f"Error validating cookies file: {e}")
        return False


def validate_url(url: str) -> bool:
    """Validate if the URL is properly formatted"""
    if not url or not isinstance(url, str):
        return False
    
    url_pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None


def get_ydl_base_opts(use_cookies: bool = True) -> dict:
    """
    Get base yt-dlp options with optional cookies support.
    
    Args:
        use_cookies: Whether to include cookies file (default: True)
    
    Returns:
        dict: Base yt-dlp options
    """
    opts = {
        "extractor_args": {
            "generic": {"impersonate": [""]}
        },
        "no_warnings": False,
        "allow_dynamic_mpd": True,
        "no_check_certificate": True,
        "geo_bypass_country": "IN",
        "ignoreerrors": False,
        "verbose": False,
        "extract_flat": False,
        "timeout": 120,
        "retries": 5,
        "sleep_interval": 1,
        "max_sleep_interval": 3,
    }
    
    # Add cookies only if file is valid
    if use_cookies and os.path.exists(cookies_file):
        try:
            with open(cookies_file, 'r') as f:
                first_line = f.readline().strip()
                if first_line.startswith("# Netscape HTTP Cookie File"):
                    opts["cookiefile"] = cookies_file
                    logger.info("Using cookies file")
        except Exception as e:
            logger.warning(f"Could not read cookies file: {e}")
    
    # Add proxy if configured
    if hasattr(Config, 'HTTP_PROXY') and Config.HTTP_PROXY and Config.HTTP_PROXY != "":
        opts["proxy"] = Config.HTTP_PROXY
    
    return opts


def extract_video_info(url: str) -> tuple[bool, dict | str]:
    """
    Extract video information WITHOUT downloading.
    This is the FIRST step - get available formats.
    
    Returns:
        tuple[bool, dict|str]: (success, info_dict_or_error_msg)
    """
    logger.info(f"Extracting info for URL: {url}")
    
    if not validate_url(url):
        return False, "Invalid URL format. Please provide a valid URL."
    
    # Ensure cookies file exists and is valid
    ensure_cookies_file()
    
    try:
        ydl_opts = get_ydl_base_opts(use_cookies=True)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info WITHOUT downloading
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:
                logger.warning("Playlist detected, using first video")
                info = info['entries'][0]
            
            return True, info
            
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if "Cloudflare anti-bot challenge" in error_msg or "HTTP Error 403" in error_msg:
            return False, "Cloudflare protection detected. Try a different URL or wait a few minutes."
        if "sign in to confirm you're not a bot" in error_msg:
            return False, "YouTube verification required. Try again in a few minutes."
        if "cookies" in error_msg.lower():
            logger.warning("Cookies error, retrying without cookies...")
            # Retry without cookies
            return extract_video_info_without_cookies(url)
        return False, f"Download error: {error_msg}"
        
    except Exception as e:
        error_msg = str(e)
        if "cookies" in error_msg.lower():
            logger.warning("Cookies error, retrying without cookies...")
            return extract_video_info_without_cookies(url)
        return False, f"Unexpected error: {error_msg}"


def extract_video_info_without_cookies(url: str) -> tuple[bool, dict | str]:
    """
    Fallback: Extract video info without using cookies.
    """
    logger.info("Attempting extraction without cookies...")
    try:
        ydl_opts = get_ydl_base_opts(use_cookies=False)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:
                logger.warning("Playlist detected, using first video")
                info = info['entries'][0]
            
            return True, info
    except Exception as e:
        return False, f"Error (no cookies): {str(e)}"


def download_specific_format(url: str, format_string: str, output_path: str) -> tuple[bool, str]:
    """
    Download video with SPECIFIC format selected by user.
    This is the SECOND step - download after user chooses quality.
    
    Args:
        url: Video URL
        format_string: Format string chosen by user (e.g., "bestvideo[height<=1080]+bestaudio/best[height<=1080]" or "best")
        output_path: Where to save the file
        
    Returns:
        tuple[bool, str]: (success, filepath_or_error_msg)
    """
    logger.info(f"Downloading format {format_string} for URL: {url}")
    
    # Ensure cookies file exists
    ensure_cookies_file()
    
    try:
        # Ensure download directory exists
        download_dir = os.path.dirname(output_path) or './downloads'
        os.makedirs(download_dir, exist_ok=True)
        
        ydl_opts = get_ydl_base_opts(use_cookies=True)
        ydl_opts.update({
            "outtmpl": output_path,
            "format": format_string,
            "merge_output_format": "mp4",
        })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            # Check if file exists (yt-dlp might add extension)
            if os.path.exists(output_path):
                return True, output_path
            
            # Check for file with different extension
            base_path = os.path.splitext(output_path)[0]
            for ext in ['.mp4', '.webm', '.mkv', '.m4a', '.mp3']:
                potential_file = base_path + ext
                if os.path.exists(potential_file):
                    return True, potential_file
            
            return False, "Download completed but file not found"
            
    except Exception as e:
        error_msg = str(e)
        if "cookies" in error_msg.lower():
            logger.warning("Cookies error during download, retrying without cookies...")
            return download_specific_format_without_cookies(url, format_string, output_path)
        return False, f"Download error: {error_msg}"


def download_specific_format_without_cookies(url: str, format_string: str, output_path: str) -> tuple[bool, str]:
    """
    Fallback: Download without cookies.
    """
    logger.info("Attempting download without cookies...")
    try:
        download_dir = os.path.dirname(output_path) or './downloads'
        os.makedirs(download_dir, exist_ok=True)
        
        ydl_opts = get_ydl_base_opts(use_cookies=False)
        ydl_opts.update({
            "outtmpl": output_path,
            "format": format_string,
            "merge_output_format": "mp4",
        })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            if os.path.exists(output_path):
                return True, output_path
            
            base_path = os.path.splitext(output_path)[0]
            for ext in ['.mp4', '.webm', '.mkv', '.m4a', '.mp3']:
                potential_file = base_path + ext
                if os.path.exists(potential_file):
                    return True, potential_file
            
            return False, "Download completed but file not found"
    except Exception as e:
        return False, f"Download error (no cookies): {str(e)}"


@Client.on_message(filters.private & filters.regex(pattern=".*http.*"))
async def echo(bot, update):
    """
    Step 1: Receive URL, extract info, show SIMPLIFIED format options (1080p or Best)
    """
    # Verification checks
    if update.from_user.id != Config.OWNER_ID:  
        if not await check_verification(bot, update.from_user.id) and Config.TRUE_OR_FALSE:
            button = [[
                InlineKeyboardButton("âœ“âƒ Vá´‡Ê€ÉªÒ“Ê âœ“âƒ", url=await get_token(bot, update.from_user.id, f"https://telegram.me/{Config.BOT_USERNAME}?start="))
                ],[
                InlineKeyboardButton("ðŸ“† Wá´€á´›á´„Êœ Há´á´¡ Tá´ Vá´‡Ê€ÉªÒ“Ê ðŸ“†", url=f"{Config.VERIFICATION}")
            ]]
            await update.reply_text(
                text="<b>PÊŸá´‡á´€sá´‡ Vá´‡Ê€ÉªÒ“Ê FÉªÊ€sá´› Tá´ Usá´‡ Má´‡</b>",
                protect_content=True,
                reply_markup=InlineKeyboardMarkup(button)
            )
            return
    
    # Logging
    if Config.LOG_CHANNEL:
        try:
            log_message = await update.forward(Config.LOG_CHANNEL)
            log_info = "Message Sender Information\n"
            log_info += "\nFirst Name: " + update.from_user.first_name
            log_info += "\nUser ID: " + str(update.from_user.id)
            log_info += "\nUsername: @" + (update.from_user.username if update.from_user.username else "")
            log_info += "\nUser Link: " + update.from_user.mention
            await log_message.reply_text(text=log_info, disable_web_page_preview=True, quote=True)
        except Exception as error:
            print(error)
    
    if not update.from_user:
        return await update.reply_text("I don't know about you sar :(")
    
    await AddUser(bot, update)
    
    if Config.UPDATES_CHANNEL:
        fsub = await handle_force_subscribe(bot, update)
        if fsub == 400:
            return

    # Parse URL (handle | separator for filename)
    url = update.text
    youtube_dl_username = None
    youtube_dl_password = None
    file_name = None

    if "|" in url:
        url_parts = url.split("|")
        if len(url_parts) == 2:
            url = url_parts[0].strip()
            file_name = url_parts[1].strip()
        elif len(url_parts) == 4:
            url = url_parts[0].strip()
            file_name = url_parts[1].strip()
            youtube_dl_username = url_parts[2].strip()
            youtube_dl_password = url_parts[3].strip()
    else:
        for entity in update.entities:
            if entity.type == "text_link":
                url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                url = url[o:o + l]

    url = url.strip()
    
    # Show processing message
    chk = await bot.send_message(
        chat_id=update.chat.id,
        text="ðŸ” Extracting video information...",
        disable_web_page_preview=True,
        reply_to_message_id=update.id,
        parse_mode=enums.ParseMode.HTML
    )

    # STEP 1: Extract info WITHOUT downloading
    success, result = extract_video_info(url)
    
    if not success:
        await chk.edit_text(f"âŒ Error: {result}")
        return
    
    response_json = result
    
    # Save info to JSON file for later use
    randem = random_char(5)
    user_session_id = f"{update.from_user.id}_{randem}"
    save_ytdl_json_path = os.path.join(
        Config.DOWNLOAD_LOCATION, 
        f"{user_session_id}.json"
    )
    
    os.makedirs(Config.DOWNLOAD_LOCATION, exist_ok=True)
    
    with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
        json.dump({
            "info": response_json,
            "url": url,
            "custom_filename": file_name,
            "session_id": user_session_id
        }, outfile, ensure_ascii=False)
    
    # Build SIMPLIFIED format selection keyboard
    inline_keyboard = []
    duration = response_json.get("duration")
    title = response_json.get("title", "Video")
    
    # Add only TWO video quality options
    inline_keyboard.append([
        InlineKeyboardButton("â”€â”€â”€â”€ ðŸŽ¬ VIDEO QUALITY â”€â”€â”€â”€", callback_data="noop")
    ])
    
    # Option 1: 1080p (if available, otherwise best available below 1080p)
    inline_keyboard.append([
        InlineKeyboardButton(
            "ðŸ“º 1080p Quality", 
            callback_data=f"dl_video|1080p|mp4|{user_session_id}"
        )
    ])
    
    # Option 2: Best Available (highest quality no matter what)
    inline_keyboard.append([
        InlineKeyboardButton(
            "ðŸŒŸ Best Available Quality", 
            callback_data=f"dl_video|best|mp4|{user_session_id}"
        )
    ])
    
    # Add audio options
    inline_keyboard.append([
        InlineKeyboardButton("â”€â”€â”€â”€ ðŸŽµ AUDIO ONLY â”€â”€â”€â”€", callback_data="noop")
    ])
    inline_keyboard.append([
        InlineKeyboardButton("ðŸŽµ Best Audio Quality", callback_data=f"dl_audio|bestaudio|m4a|{user_session_id}")
    ])
    
    # Add MP3 conversion options
    inline_keyboard.append([
        InlineKeyboardButton("â”€â”€â”€â”€ ðŸŽ¼ CONVERT TO MP3 â”€â”€â”€â”€", callback_data="noop")
    ])
    inline_keyboard.append([
        InlineKeyboardButton("ðŸŽµ MP3 128kbps", callback_data=f"dl_mp3|128|mp3|{user_session_id}"),
        InlineKeyboardButton("ðŸŽµ MP3 320kbps", callback_data=f"dl_mp3|320|mp3|{user_session_id}")
    ])
    
    # Add close button
    inline_keyboard.append([                 
        InlineKeyboardButton("ðŸ”’ Close", callback_data='close')               
    ])
    
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    
    await chk.delete()
    await bot.send_message(
        chat_id=update.chat.id,
        text=f"<b>ðŸ“¹ {title}</b>\n\n"
             f"â± Duration: {TimeFormatter(duration * 1000) if duration else 'Unknown'}\n\n"
             f"<b>Select quality to download:</b>\n"
             f"â€¢ <i>1080p Quality</i> - Download in 1080p if available, or best quality below 1080p\n"
             f"â€¢ <i>Best Available</i> - Download the highest quality available (480p/1080p/4K/etc)",
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        reply_to_message_id=update.id,
        parse_mode=enums.ParseMode.HTML
    )


@Client.on_callback_query(filters.regex("^dl_"))
async def download_callback(bot, query):
    """
    Step 2: User clicked quality button - now download and upload
    """
    try:
        # Parse callback data: dl_type|format_id|ext|session_id
        data_parts = query.data.split("|")
        if len(data_parts) != 4:
            await query.answer("Invalid selection", show_alert=True)
            return
        
        dl_type, format_id, ext, session_id = data_parts
        
        # Load saved video info
        json_path = os.path.join(Config.DOWNLOAD_LOCATION, f"{session_id}.json")
        
        if not os.path.exists(json_path):
            await query.answer("Session expired. Please send URL again.", show_alert=True)
            return
        
        with open(json_path, "r", encoding="utf8") as f:
            session_data = json.load(f)
        
        url = session_data["url"]
        info = session_data["info"]
        custom_filename = session_data.get("custom_filename")
        
        # Build the format string based on user selection
        if format_id == "1080p":
            # Try 1080p, fallback to best available below 1080p
            format_string = "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
            quality_label = "1080p"
        elif format_id == "best":
            # Best available quality (no limit)
            format_string = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
            quality_label = "Best Available"
        elif format_id == "bestaudio":
            # Best audio
            format_string = "bestaudio/best"
            quality_label = "Best Audio"
        else:
            # Fallback
            format_string = format_id
            quality_label = format_id
        
        # Update message to show downloading
        await query.edit_message_text(
            f"â¬‡ï¸ Downloading in <b>{quality_label}</b> quality...\n\n"
            f"<i>Please wait, this may take a while...</i>",
            parse_mode=enums.ParseMode.HTML
        )
        
        # Determine output filename
        title = info.get("title", "video")
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        
        if custom_filename:
            base_filename = custom_filename
        else:
            base_filename = f"{safe_title[:50]}"  # Limit length
        
        output_path = os.path.join(
            Config.DOWNLOAD_LOCATION,
            f"{session_id}_{base_filename}.{ext}"
        )
        
        # Handle different download types
        if dl_type == "dl_mp3":
            # MP3 conversion: extract audio and convert
            bitrate = format_id  # format_id contains bitrate for MP3
            output_path = output_path.replace(f".{ext}", ".mp3")
            
            # Download with audio extraction
            success, filepath = download_with_mp3_conversion(url, output_path, bitrate)
        else:
            # Regular download with selected format
            success, filepath = download_specific_format(url, format_string, output_path)
        
        if not success:
            await query.edit_message_text(f"âŒ Download failed: {filepath}")
            return
        
        # Check file size
        file_size = os.path.getsize(filepath)
        if file_size > 2097152000:  # 2GB Telegram limit
            await query.edit_message_text(
                f"âŒ File too large: {humanbytes(file_size)}\n"
                f"Telegram limit is 2GB"
            )
            os.remove(filepath)
            return
        
        # Upload to Telegram
        await query.edit_message_text(
            f"ðŸ“¤ Uploading {humanbytes(file_size)}...",
            parse_mode=enums.ParseMode.HTML
        )
        
        # Determine upload type
        if dl_type == "dl_audio" or dl_type == "dl_mp3":
            # Upload as audio
            duration = info.get("duration", 0)
            performer = info.get("uploader", "Unknown")
            title_track = info.get("title", "Audio")
            
            await bot.send_audio(
                chat_id=query.message.chat.id,
                audio=filepath,
                duration=duration,
                performer=performer,
                title=title_track,
                progress=progress_for_pyrogram,
                progress_args=(
                    f"ðŸ“¤ Uploading {os.path.basename(filepath)}",
                    query.message,
                    time.time()
                )
            )
        else:
            # Upload as video
            duration = info.get("duration", 0)
            width = info.get("width", 1280)
            height = info.get("height", 720)
            
            # Generate thumbnail if possible
            thumb_path = None
            if info.get("thumbnail"):
                try:
                    thumb_path = os.path.join(Config.DOWNLOAD_LOCATION, f"{session_id}_thumb.jpg")
                    response = requests.get(info["thumbnail"], timeout=10)
                    with open(thumb_path, "wb") as thumb_file:
                        thumb_file.write(response.content)
                except:
                    thumb_path = None
            
            await bot.send_video(
                chat_id=query.message.chat.id,
                video=filepath,
                duration=duration,
                width=width,
                height=height,
                thumb=thumb_path,
                caption=f"<b>{info.get('title', 'Video')}</b>\n\n<i>Quality: {quality_label}</i>",
                parse_mode=enums.ParseMode.HTML,
                progress=progress_for_pyrogram,
                progress_args=(
                    f"ðŸ“¤ Uploading {os.path.basename(filepath)}",
                    query.message,
                    time.time()
                )
            )
            
            # Cleanup thumbnail
            if thumb_path and os.path.exists(thumb_path):
                os.remove(thumb_path)
        
        # Cleanup files
        os.remove(filepath)
        if os.path.exists(json_path):
            os.remove(json_path)
        
        # Delete status message
        await query.message.delete()
        await query.answer("âœ… Uploaded successfully!", show_alert=False)
        
    except Exception as e:
        logger.error(f"Callback error: {e}")
        await query.answer(f"Error: {str(e)}", show_alert=True)


def download_with_mp3_conversion(url: str, output_path: str, bitrate: str) -> tuple[bool, str]:
    """
    Download and convert to MP3 with specified bitrate
    """
    # Ensure cookies file exists
    ensure_cookies_file()
    
    try:
        ydl_opts = get_ydl_base_opts(use_cookies=True)
        ydl_opts.update({
            "outtmpl": output_path,
            "format": "bestaudio/best",
            "postprocessors": [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate,
            }],
        })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            # yt-dlp adds .mp3 extension after conversion
            if os.path.exists(output_path):
                return True, output_path
            
            # Check without original extension
            base = os.path.splitext(output_path)[0]
            if os.path.exists(f"{base}.mp3"):
                return True, f"{base}.mp3"
            
            return False, "Conversion completed but file not found"
    
    except Exception as e:
        error_msg = str(e)
        if "cookies" in error_msg.lower():
            logger.warning("Cookies error during MP3 conversion, retrying without cookies...")
            return download_with_mp3_conversion_without_cookies(url, output_path, bitrate)
        return False, f"Conversion error: {error_msg}"


def download_with_mp3_conversion_without_cookies(url: str, output_path: str, bitrate: str) -> tuple[bool, str]:
    """
    Fallback: Download and convert to MP3 without cookies.
    """
    logger.info("Attempting MP3 conversion without cookies...")
    try:
        ydl_opts = get_ydl_base_opts(use_cookies=False)
        ydl_opts.update({
            "outtmpl": output_path,
            "format": "bestaudio/best",
            "postprocessors": [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate,
            }],
        })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            if os.path.exists(output_path):
                return True, output_path
            
            base = os.path.splitext(output_path)[0]
            if os.path.exists(f"{base}.mp3"):
                return True, f"{base}.mp3"
            
            return False, "Conversion completed but file not found"
    except Exception as e:
        return False, f"Conversion error (no cookies): {str(e)}"


@Client.on_callback_query(filters.regex("^close$"))
async def close_callback(bot, query):
    """Close button handler"""
    await query.message.delete()
    await query.answer("Closed", show_alert=False)
