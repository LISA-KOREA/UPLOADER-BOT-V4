# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | TG-SORRY
# Full quality selection (720p–4K), multi-codec variants, best audio enforced, rename support.
# Assumptions: aria2c preferred for speed; best audio will be merged for video formats.

import logging
import os
import asyncio
import json
from pyrogram import filters, enums, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
import yt_dlp

from plugins.config import Config
from plugins.script import Translation
from plugins.functions.verify import check_verification, get_token
from plugins.functions.forcesub import handle_force_subscribe
from plugins.functions.display_progress import humanbytes, TimeFormatter
from plugins.functions.ran_text import random_char
from plugins.database.add import AddUser

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("yt_dlp").setLevel(logging.DEBUG)

os.makedirs(Config.DOWNLOAD_LOCATION, exist_ok=True)
cookies_file = 'cookies.txt' if os.path.exists('cookies.txt') else None

def _codec_short(vcodec: str) -> str:
    if not vcodec or vcodec == 'none':
        return ""
    vcodec = vcodec.lower()
    if "av01" in vcodec or "av1" in vcodec:
        return "AV1"
    if "vp9" in vcodec:
        return "VP9"
    if "hvc1" in vcodec or "hevc" in vcodec or "hev1" in vcodec:
        return "HEVC"
    if "avc1" in vcodec or "h264" in vcodec:
        return "H264"
    return vcodec.split(".")[0].upper()

def _estimate_size(fmt: dict, duration: int, best_audio: dict = None) -> int:
    fs = fmt.get("filesize") or fmt.get("filesize_approx")
    if fs:
        return int(fs)
    if duration <= 0:
        return 0
    total_bits_per_sec = 0.0
    v_tbr = fmt.get("tbr") or fmt.get("vbr")
    if v_tbr:
        try:
            total_bits_per_sec += float(v_tbr) * 1000
        except Exception:
            pass
    if fmt.get("acodec") == "none":
        if best_audio:
            a_abr = best_audio.get("abr") or best_audio.get("tbr") or best_audio.get("vbr")
            if a_abr:
                try:
                    total_bits_per_sec += float(a_abr) * 1000
                except Exception:
                    pass
        else:
            total_bits_per_sec += 128_000
    if total_bits_per_sec <= 0:
        return 0
    total_bits = total_bits_per_sec * duration
    total_bytes = int(total_bits / 8)
    return total_bytes

async def _extract_info(url: str):
    def _do():
        try:
            ydl_opts = {
                "extractor_args": {"generic": {"impersonate": [""]}},
                "noplaylist": True,
                "no_warnings": True,
                "quiet": True,
                "allow_dynamic_mpd": True,
                "no_check_certificate": True,
                "geo_bypass_country": "IN",
                "ignoreerrors": False,
            }
            if cookies_file:
                ydl_opts["cookiefile"] = cookies_file
            if getattr(Config, "HTTP_PROXY", None):
                ydl_opts["proxy"] = Config.HTTP_PROXY
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    return None
                if "entries" in info:
                    for entry in info["entries"]:
                        if entry and (entry.get("formats") or entry.get("url")):
                            info = entry
                            break
                    else:
                        return None
                return info
        except Exception as e:
            logger.exception("yt_dlp extract error: %s", e)
            return None

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _do)

@Client.on_message(filters.private & filters.regex(pattern=".*http.*"))
async def echo(bot, update):
    if update.from_user.id != Config.OWNER_ID:
        if not await check_verification(bot, update.from_user.id) and Config.TRUE_OR_FALSE:
            button = [[
                InlineKeyboardButton("✓⃝ Vᴇʀɪꜰʏ ✓⃝", url=await get_token(bot, update.from_user.id, f"https://telegram.me/{Config.BOT_USERNAME}?start="))
            ], [
                InlineKeyboardButton("📆 Wᴀᴛᴄʜ Hᴏᴡ Tᴏ Vᴇʀɪꜰʏ 📆", url=f"{Config.VERIFICATION}")
            ]]
            await update.reply_text(text="Pʟᴇᴀsᴇ Vᴇʀɪꜰʏ Fɪʀsᴛ Tᴏ Usᴇ Mᴇ", protect_content=True, reply_markup=InlineKeyboardMarkup(button))
            return

    await AddUser(bot, update)
    if Config.UPDATES_CHANNEL:
        try:
            if await handle_force_subscribe(bot, update) == 400:
                return
        except UserNotParticipant:
            return

    raw = update.text.strip()
    url = raw
    user_file_name = None
    youtube_dl_username = None
    youtube_dl_password = None

    if "|" in raw:
        parts = raw.split("|")
        if len(parts) == 2:
            url, user_file_name = parts[0].strip(), parts[1].strip()
        elif len(parts) == 4:
            url, user_file_name, youtube_dl_username, youtube_dl_password = [p.strip() for p in parts]
    else:
        for ent in update.entities:
            if ent.type == "text_link":
                url = ent.url
            elif ent.type == "url":
                o, l = ent.offset, ent.length
                url = raw[o:o + l]

    chk = await bot.send_message(chat_id=update.chat.id, text=Translation.DOWNLOAD_START, disable_web_page_preview=True, reply_to_message_id=update.id)

    info = await _extract_info(url)
    if info is None:
        await chk.edit_text("❌ Failed to extract video info. Please check the URL.")
        return

    title = info.get("title", "Video")
    duration = info.get("duration", 0) or 0
    formats = info.get("formats", [])

    audio_streams = [f for f in formats if f.get("vcodec") == "none" and f.get("acodec") != "none"]
    audio_streams.sort(key=lambda f: (f.get("abr") or f.get("tbr") or 0), reverse=True)
    best_audio = audio_streams[0] if audio_streams else None
    best_audio_id = best_audio.get("format_id") if best_audio else None

    target_heights = [2160, 1440, 1080, 720]
    seen_per_height = {}
    quality_buttons = []

    for fmt in formats:
        vcodec = fmt.get("vcodec", "none")
        if vcodec == "none":
            continue
        height = fmt.get("height", 0) or 0
        if height not in target_heights:
            continue

        fmt_id = fmt.get("format_id")
        ext = fmt.get("ext", "mp4")

        if fmt.get("acodec") == "none" and best_audio_id and best_audio_id not in fmt_id.split("+"):
            combined_id = f"{fmt_id}+{best_audio_id}"
        else:
            combined_id = fmt_id

        codec_label = _codec_short(vcodec)
        size_bytes = _estimate_size(fmt, duration, best_audio)
        size_text = humanbytes(size_bytes) if size_bytes else "≈?"

        variants = seen_per_height.setdefault(height, [])
        if codec_label in [v["codec"] for v in variants]:
            continue
        if len(variants) >= 3:
            continue

        variants.append({"codec": codec_label, "id": combined_id})
        label = f"{height}p • {ext.upper()}"
        if codec_label:
            label += f" • {codec_label}"
        label += f" • {size_text}"

        cb_string = f"video|{combined_id}|{ext}|{random_char(5)}"
        quality_buttons.append([InlineKeyboardButton(label, callback_data=cb_string)])

    if not quality_buttons:
        best_fmt = None
        for f in formats:
            if f.get("vcodec") != "none":
                if not best_fmt or (f.get("height") or 0) > (best_fmt.get("height") or 0):
                    best_fmt = f
        if best_fmt:
            ext = best_fmt.get("ext", "mp4")
            b_id = best_fmt.get("format_id")
            if best_fmt.get("acodec") == "none" and best_audio_id:
                b_id = f"{b_id}+{best_audio_id}"
            est = _estimate_size(best_fmt, duration, best_audio)
            label = f"Best ({best_fmt.get('height','?')}p) • {ext.upper()} • {humanbytes(est) if est else '≈?'}"
            cb_string = f"video|{b_id}|{ext}|{random_char(5)}"
            quality_buttons.append([InlineKeyboardButton(label, callback_data=cb_string)])

    if best_audio:
        audio_cb = f"audio|bestaudio|mp3|{random_char(5)}"
        quality_buttons.append([InlineKeyboardButton("🎵 Best Audio (auto quality)", callback_data=audio_cb)])

    quality_buttons.append([InlineKeyboardButton("🔒 Close", callback_data="close")])
    reply_markup = InlineKeyboardMarkup(quality_buttons)

    session_rand = random_char(5)
    info["_preferred_name"] = (user_file_name.strip() if user_file_name else title)[:180]
    session_path = os.path.join(Config.DOWNLOAD_LOCATION, f"{update.from_user.id}{session_rand}.json")
    with open(session_path, "w", encoding="utf8") as out:
        json.dump(info, out, ensure_ascii=False)

    fixed_keyboard = []
    for row in quality_buttons:
        btn = row[0]
        parts = btn.callback_data.split("|")
        parts[-1] = session_rand
        fixed_keyboard.append([InlineKeyboardButton(btn.text, callback_data="|".join(parts))])

    await chk.delete()
    await bot.send_message(
        chat_id=update.chat.id,
        text=f"📹 **{title}**\n\n⏱ Duration: {TimeFormatter(duration*1000) if duration else 'Unknown'}\n\nSelect quality (auto merges best audio):",
        reply_markup=InlineKeyboardMarkup(fixed_keyboard),
        parse_mode=enums.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_to_message_id=update.id
    )
