# Yt-dlp download with aria2c preferred (graceful fallback), live unified progress,
# Pause/Resume/Cancel inline controls, and MediaInfo card before upload.
# Supports rename via _preferred_name and best audio merging for video formats.
# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL

import logging
import asyncio
import json
import os
import shutil
import time
import re
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.config import Config
from plugins.script import Translation
from plugins.thumbnail import *
from plugins.functions.display_progress import progress_for_pyrogram, humanbytes, download_progress_edit
from plugins.database.database import db
from plugins.functions.ran_text import random_char
from plugins.functions.media_info import extract_media_summary, format_media_summary
from plugins.functions.task_runtime import set_task, get_task, del_task

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

cookies_file = 'cookies.txt' if os.path.exists('cookies.txt') else None

def sanitize_filename(name: str) -> str:
    name = name.split("?")[0].split("#")[0]
    for c in ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*', ';', '&', '=']:
        name = name.replace(c, '_')
    name = name.strip().strip('.')
    if len(name) > 200:
        n, e = os.path.splitext(name)
        name = n[:195] + e
    return name or "download.mp4"

def aria2c_available() -> bool:
    try:
        import subprocess
        r = subprocess.run(["aria2c", "--version"], capture_output=True, text=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False

ARIA = aria2c_available()

def task_keyboard(paused: bool, task_id: str):
    rows = []
    if paused:
        rows.append([InlineKeyboardButton("▶ Resume", callback_data=f"task|resume|{task_id}"),
                     InlineKeyboardButton("⏹ Cancel", callback_data=f"task|cancel|{task_id}")])
    else:
        rows.append([InlineKeyboardButton("⏸ Pause", callback_data=f"task|pause|{task_id}"),
                     InlineKeyboardButton("⏹ Cancel", callback_data=f"task|cancel|{task_id}")])
    rows.append([InlineKeyboardButton("ℹ️ Media Info", callback_data=f"task|mediainfo|{task_id}")])
    return InlineKeyboardMarkup(rows)

async def youtube_dl_call_back(bot, update):
    cb_data = update.data
    try:
        tg_send_type, fmt_string, ext_hint, session_tag = cb_data.split("|")
    except Exception:
        logger.error("Invalid callback data: %s", cb_data)
        return False

    session_path = os.path.join(Config.DOWNLOAD_LOCATION, f"{update.from_user.id}{session_tag}.json")
    try:
        with open(session_path, "r", encoding="utf8") as f:
            info = json.load(f)
    except Exception:
        try:
            await update.message.edit_caption("❌ Session expired. Send URL again.")
        except:
            await update.message.edit_text("❌ Session expired. Send URL again.")
        return False

    original_url = update.message.reply_to_message.text.strip()
    preferred = info.get("_preferred_name") or info.get("title") or "video"
    base_name = sanitize_filename(preferred)
    tmp_dir = os.path.join(Config.DOWNLOAD_LOCATION, f"{update.from_user.id}{random_char(5)}")
    os.makedirs(tmp_dir, exist_ok=True)
    output_template = os.path.join(tmp_dir, f"{base_name}.%(ext)s")
    display_name = f"{base_name}.{ext_hint}"

    task_id = f"{update.from_user.id}-{update.message.id}-{random_char(5)}"
    start_caption = Translation.DOWNLOAD_START.format(display_name)
    if not ARIA:
        start_caption += "\n\n⚠️ aria2c not found – using default downloader."
    try:
        await update.message.edit_caption(start_caption, reply_markup=task_keyboard(False, task_id))
    except Exception:
        try:
            await update.message.edit_text(start_caption, reply_markup=task_keyboard(False, task_id))
        except Exception:
            pass

    if tg_send_type == "audio":
        command = [
            "yt-dlp", "-c", "--newline", "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
            "-f", "bestaudio/best",
            "--extract-audio", "--audio-format", ext_hint, "--audio-quality", "0",
            "-o", output_template,
            "--buffer-size", "16K", "--http-chunk-size", "10M", "--retries", "10", "--fragment-retries", "10",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ]
    else:
        command = [
            "yt-dlp", "-c", "--newline", "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
            "-f", fmt_string,
            "-o", output_template,
            "--buffer-size", "16K", "--http-chunk-size", "10M", "--retries", "10", "--fragment-retries", "10",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ]

    if cookies_file:
        command.extend(["--cookies", cookies_file])
    if getattr(Config, "HTTP_PROXY", None):
        command.extend(["--proxy", Config.HTTP_PROXY])

    if ARIA:
        command.extend([
            "--external-downloader", "aria2c",
            "--external-downloader-args",
            "-x 16 -s 16 -k 1M --max-connection-per-server=16 --min-split-size=1M --console-log-level=warn"
        ])
        prefix = "⬇️ Downloading (aria2c 🚀)"
    else:
        command.extend(["-N", "8"])
        prefix = "⬇️ Downloading"

    command.append(original_url)
    logger.debug("Command: %s", " ".join(command))

    start_ts = time.time()
    process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)

    await set_task(task_id, {
        "task_id": task_id,
        "user_id": update.from_user.id,
        "command": command,
        "process": process,
        "tmp_dir": tmp_dir,
        "output_template": output_template,
        "display_name": display_name,
        "status": "downloading",
        "chat_id": update.message.chat.id,
        "message_id": update.message.id,
        "message": update.message,
        "prefix": prefix,
        "start_ts": start_ts,
        "downloaded_file": None
    })

    aria_pattern = re.compile(r'\[#\d+\s+SIZE:(?P<size_done>[\d\.]+\w+)/(?P<size_total>[\d\.]+\w+)\((?P<pct>\d+)%)\s+CN:\d+\s+DL:(?P<speed>[\d\.]+\w+/s)')
    ytdlp_patterns = [
        re.compile(r'\[download\]\s+(\d{1,3}\.\d+)%\s+of\s+~?([\d\.]+\w+)\s+at\s+([\d\.]+\w+/s)'),
        re.compile(r'\[download\]\s+(\d{1,3}\.\d+)%')
    ]

    async def reader():
        last = None
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            s = line.decode(errors='ignore').strip()
            percent = None; size_str = None; speed_str = None
            m0 = aria_pattern.search(s)
            if m0:
                try:
                    percent = float(m0.group("pct"))
                except Exception:
                    percent = None
                size_str = f"{m0.group('size_done')} / {m0.group('size_total')}"
                speed_str = m0.group("speed")
            else:
                for pat in ytdlp_patterns:
                    m = pat.search(s)
                    if m:
                        try:
                            percent = float(m.group(1))
                        except Exception:
                            percent = None
                        if len(m.groups()) >= 2:
                            size_str = m.group(2)
                        if len(m.groups()) >= 3:
                            speed_str = m.group(3)
                        break
            if percent is not None and (last is None or percent - last >= 0.5):
                await download_progress_edit(update.message, display_name, percent, size_str, speed_str, start_ts, min_interval=1.0, status_prefix=prefix)
                last = percent

    reader_task = asyncio.create_task(reader())
    await process.wait()
    await reader_task

    task = await get_task(task_id)
    if not task or task.get("status") in ("paused", "canceled"):
        return

    downloaded = None
    for root, _, files in os.walk(tmp_dir):
        for f in files:
            if f.endswith(".json"):
                continue
            cand = os.path.join(root, f)
            if not downloaded or os.path.getsize(cand) > os.path.getsize(downloaded):
                downloaded = cand

    if process.returncode != 0 or not downloaded or not os.path.isfile(downloaded):
        try:
            await update.message.edit_caption("❌ Download failed.")
        except Exception:
            try:
                await update.message.edit_text("❌ Download failed.")
            except Exception:
                pass
        try:
            await del_task(task_id)
            shutil.rmtree(tmp_dir)
        except Exception:
            pass
        return False

    task["downloaded_file"] = downloaded
    await set_task(task_id, task)

    file_size = os.path.getsize(downloaded)
    dl_time = int(time.time() - start_ts)

    if file_size > Config.TG_MAX_FILE_SIZE:
        msg = Translation.RCHD_TG_API_LIMIT.format(dl_time, humanbytes(file_size))
        try:
            await update.message.edit_caption(msg)
        except Exception:
            try:
                await update.message.edit_text(msg)
            except Exception:
                pass
        try:
            await del_task(task_id)
            shutil.rmtree(tmp_dir)
        except Exception:
            pass
        return False

    media_summary = extract_media_summary(downloaded)
    media_text = format_media_summary(media_summary)
    try:
        await update.message.edit_caption(f"{Translation.UPLOAD_START.format(os.path.basename(downloaded))}\n\n{media_text}", reply_markup=task_keyboard(False, task_id))
    except Exception:
        try:
            await update.message.edit_text(f"{Translation.UPLOAD_START.format(os.path.basename(downloaded))}\n\n{media_text}", reply_markup=task_keyboard(False, task_id))
        except Exception:
            pass

    up_start = time.time()
    description = Translation.CUSTOM_CAPTION_UL_FILE
    if info.get("fulltitle"):
        description = info["fulltitle"][:1021]
    elif info.get("title"):
        description = info["title"][:1021]
    elif info.get("description"):
        description = info["description"][:1021]

    try:
        if tg_send_type == "audio":
            duration = await Mdata03(downloaded)
            thumb = await Gthumb01(bot, update)
            await update.message.reply_audio(audio=downloaded, caption=description, duration=duration, thumb=thumb, progress=progress_for_pyrogram, progress_args=(Translation.UPLOAD_START, update.message, up_start))
        elif tg_send_type == "vm":
            width, duration = await Mdata02(downloaded)
            thumb = await Gthumb02(bot, update, duration, downloaded)
            await update.message.reply_video_note(video_note=downloaded, duration=duration, length=width, thumb=thumb, progress=progress_for_pyrogram, progress_args=(Translation.UPLOAD_START, update.message, up_start))
        else:
            if not await db.get_upload_as_doc(update.from_user.id):
                thumb = await Gthumb01(bot, update)
                await update.message.reply_document(document=downloaded, thumb=thumb, caption=description, progress=progress_for_pyrogram, progress_args=(Translation.UPLOAD_START, update.message, up_start))
            else:
                width, height, duration = await Mdata01(downloaded)
                thumb = await Gthumb02(bot, update, duration, downloaded)
                await update.message.reply_video(video=downloaded, caption=description, duration=duration, width=width, height=height, supports_streaming=True, thumb=thumb, progress=progress_for_pyrogram, progress_args=(Translation.UPLOAD_START, update.message, up_start))
        up_time = int(time.time() - up_start)

        try:
            shutil.rmtree(tmp_dir)
        except Exception:
            pass

        final_msg = Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(dl_time, up_time)
        if ARIA:
            final_msg += " (aria2c 🚀)"

        compact = []
        if media_summary.get("width") and media_summary.get("height"):
            compact.append(f"{media_summary['width']}x{media_summary['height']}")
        if media_summary.get("video_codec"):
            compact.append(media_summary["video_codec"].upper())
        if media_summary.get("audio_codec"):
            compact.append(media_summary["audio_codec"].upper())
        if media_summary.get("bitrate_kbps"):
            compact.append(f"{media_summary['bitrate_kbps']}kbps")
        compact.append(media_summary.get("size_human", ""))
        final_msg += "\n\n" + " • ".join([p for p in compact if p])

        try:
            await update.message.edit_caption(final_msg, reply_markup=task_keyboard(True, task_id))
        except Exception:
            try:
                await update.message.edit_text(final_msg, reply_markup=task_keyboard(True, task_id))
            except Exception:
                pass

        await del_task(task_id)
        return True

    except Exception as e:
        logger.exception("Upload failed: %s", e)
        try:
            await update.message.edit_caption(f"❌ Upload failed: {e}")
        except Exception:
            try:
                await update.message.edit_text(f"❌ Upload failed: {e}")
            except Exception:
                pass
        try:
            shutil.rmtree(tmp_dir)
        except Exception:
            pass
        await del_task(task_id)
        return False
