# Callback handlers for Pause/Resume/Cancel and Media Info buttons.
import asyncio
import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.functions.task_runtime import get_task, set_task, del_task
from plugins.functions.display_progress import download_progress_edit
from plugins.functions.media_info import extract_media_summary, format_media_summary

logger = logging.getLogger(__name__)

def _kb(paused: bool, task_id: str):
    rows = []
    if paused:
        rows.append([
            InlineKeyboardButton("▶ Resume", callback_data=f"task|resume|{task_id}"),
            InlineKeyboardButton("⏹ Cancel", callback_data=f"task|cancel|{task_id}")
        ])
    else:
        rows.append([
            InlineKeyboardButton("⏸ Pause", callback_data=f"task|pause|{task_id}"),
            InlineKeyboardButton("⏹ Cancel", callback_data=f"task|cancel|{task_id}")
        ])
    rows.append([InlineKeyboardButton("ℹ️ Media Info", callback_data=f"task|mediainfo|{task_id}")])
    return InlineKeyboardMarkup(rows)


@Client.on_callback_query(filters.regex(r"^task\|"))
async def task_control(client, cq):
    try:
        _, action, task_id = cq.data.split("|", 2)
    except Exception:
        await cq.answer("Invalid task action", show_alert=True)
        return

    task = await get_task(task_id)
    if not task:
        await cq.answer("Task not found (maybe finished).", show_alert=True)
        return

    msg = task.get("message")
    if not msg:
        await cq.answer("Message not available.", show_alert=True)
        return

    if action == "pause":
        proc = task.get("process")
        if proc and getattr(proc, "returncode", None) is None:
            try:
                proc.terminate()
            except ProcessLookupError:
                pass
            await cq.answer("Paused. You can resume anytime.")
            task["status"] = "paused"
            await set_task(task_id, task)
            try:
                await msg.edit_caption(f"{task.get('prefix','⬇️ Downloading')} (paused)\n\n📁 {task.get('display_name')}", reply_markup=_kb(True, task_id))
            except Exception:
                try:
                    await msg.edit_text(f"{task.get('prefix','⬇️ Downloading')} (paused)\n\n📁 {task.get('display_name')}", reply_markup=_kb(True, task_id))
                except Exception:
                    pass
        else:
            await cq.answer("Task is not running.", show_alert=True)

    elif action == "resume":
        if task.get("status") != "paused":
            await cq.answer("Task is not paused.", show_alert=True)
            return

        cmd = task.get("command")
        if not cmd:
            await cq.answer("No resume command stored.", show_alert=True)
            return

        await cq.answer("Resuming…")

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        task["process"] = process
        task["status"] = "downloading"
        await set_task(task_id, task)

        async def reader():
            import re, time
            start_ts = task.get("start_ts") or time.time()
            patterns = [
                re.compile(r'\[#\d+\s+SIZE:(?P<size_done>[\d\.]+\w+)/(?P<size_total>[\d\.]+\w+)\((?P<pct>\d+)%\)\s+CN:\d+\s+DL:(?P<speed>[\d\.]+\w+/s)'),
                re.compile(r'\[download\]\s+(\d{1,3}\.\d+)%\s+of\s+~?(\[\d\.]+\w+)\s+at\s+([\d\.]+\w+/s)') ,
                re.compile(r'\[download\]\s+(\d{1,3}\.\d+)%')
            ]
            last = None
            prefix = task.get("prefix", "⬇️ Downloading")
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                s = line.decode(errors='ignore').strip()
                percent = None; size_str = None; speed_str = None
                m0 = patterns[0].search(s)
                if m0:
                    try:
                        percent = float(m0.group("pct"))
                    except Exception:
                        percent = None
                    size_str = f"{m0.group('size_done')} / {m0.group('size_total')}"
                    speed_str = m0.group("speed")
                else:
                    for pat in patterns[1:]:
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
                    await download_progress_edit(task["message"], task.get("display_name"), percent, size_str, speed_str, start_ts, min_interval=1.0, status_prefix=prefix)
                    last = percent

        asyncio.create_task(reader())

        try:
            await msg.edit_caption(f"{task.get('prefix','⬇️ Downloading')}\n\n📁 {task.get('display_name')}", reply_markup=_kb(False, task_id))
        except Exception:
            try:
                await msg.edit_text(f"{task.get('prefix','⬇️ Downloading')}\n\n📁 {task.get('display_name')}", reply_markup=_kb(False, task_id))
            except Exception:
                pass

    elif action == "cancel":
        proc = task.get("process")
        if proc and getattr(proc, "returncode", None) is None:
            try:
                proc.terminate()
            except ProcessLookupError:
                pass
        tmp_dir = task.get("tmp_dir")
        if tmp_dir and os.path.isdir(tmp_dir):
            try:
                import shutil; shutil.rmtree(tmp_dir)
            except Exception:
                pass
        await del_task(task_id)
        await cq.answer("Canceled and cleaned.")
        try:
            await msg.edit_caption("❌ Task canceled.")
        except Exception:
            try:
                await msg.edit_text("❌ Task canceled.")
            except Exception:
                pass

    elif action == "mediainfo":
        path = task.get("downloaded_file")
        if not path or not os.path.exists(path):
            await cq.answer("File not ready yet.", show_alert=True)
            return
        summary = extract_media_summary(path)
        text = format_media_summary(summary)
        await cq.answer()
        try:
            await msg.reply_text(text, disable_web_page_preview=True)
        except Exception:
            pass
