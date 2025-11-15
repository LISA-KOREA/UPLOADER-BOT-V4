import time
import asyncio
import logging

logger = logging.getLogger(__name__)

_last_download_update = {}
_lock = asyncio.Lock()

def humanbytes(size: int) -> str:
    if size is None or size <= 0:
        return "0B"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024.0
        i += 1
    return f"{size:.2f} {units[i]}"

def TimeFormatter(milliseconds: int) -> str:
    seconds, _ = divmod(int(milliseconds), 1000)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h {m}m {s}s"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"

async def download_progress_edit(message, file_name: str,
                                 percent: float = None,
                                 size_str: str = None,
                                 speed_str: str = None,
                                 start_time: float = None,
                                 min_interval: float = 1.2,
                                 status_prefix: str = "⬇️ Downloading"):
    try:
        key = f"{message.chat.id}:{message.message_id}"
    except Exception:
        return
    now = time.time()
    async with _lock:
        last = _last_download_update.get(key, 0.0)
        if now - last < min_interval:
            return
        _last_download_update[key] = now

    lines = [status_prefix, "", f"📁 {file_name}", ""]
    if percent is not None:
        try:
            lines.append(f"Progress: {percent:.1f}%")
        except Exception:
            lines.append(f"Progress: {percent}")
    if size_str:
        lines.append(f"Size: {size_str}")
    if speed_str:
        lines.append(f"Speed: {speed_str}")
    if start_time and percent and percent > 0:
        elapsed = now - start_time
        try:
            total_time = (elapsed / percent) * 100
            eta = int(total_time - elapsed)
            if eta > 0:
                lines.append(f"ETA: {eta//60}m {eta%60}s")
        except Exception:
            pass
    caption = "\n".join(lines)
    try:
        await message.edit_caption(caption=caption)
    except Exception:
        try:
            await message.edit_text(caption)
        except Exception as e:
            logger.debug(f"Failed to edit progress message: {e}")

# Backward-compatible upload progress helper:
# Accepts either:
# - progress_for_pyrogram(current, total, ud_type, message, start)
# - progress_for_pyrogram(current, total, message, start)
async def progress_for_pyrogram(current, total, *args):
    ud_type = None
    message = None
    start = None
    if len(args) == 3:
        # legacy: (ud_type, message, start)
        ud_type, message, start = args
    elif len(args) == 2:
        message, start = args
    else:
        return

    percent = 0
    if total:
        try:
            percent = (current / total) * 100
        except Exception:
            percent = 0
    size_str = f"{humanbytes(current)} / {humanbytes(total)}" if total else humanbytes(current)
    speed_str = ""
    try:
        elapsed = time.time() - start
        if elapsed > 0:
            speed_str = f"{humanbytes(int(current / elapsed))}/s"
    except Exception:
        pass
    prefix = f"📤 Uploading" if not ud_type else f"📤 Uploading — {ud_type}"
    await download_progress_edit(
        message,
        getattr(message, "file_name", "file"),
        percent,
        size_str,
        speed_str,
        start,
        min_interval=1.0,
        status_prefix=prefix
    )
