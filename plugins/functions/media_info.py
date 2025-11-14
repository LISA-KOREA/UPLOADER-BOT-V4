"""
Media info utilities using ffprobe (recommended) with graceful fallback.

Functions:
- probe_media(path) -> dict (raw ffprobe JSON or empty dict)
- extract_media_summary(path) -> dict with normalized fields
- format_media_summary(summary) -> human-readable multiline string

Requires: ffprobe in PATH (from ffmpeg). Install: apt-get install -y ffmpeg
If ffprobe is missing, functions fall back to basic size/duration heuristics.
"""
import subprocess
import json
import shlex
import os

def probe_media(path: str) -> dict:
    if not os.path.isfile(path):
        return {}
    cmd = f'ffprobe -v quiet -print_format json -show_format -show_streams {shlex.quote(path)}'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            return {}
        return json.loads(result.stdout.strip() or '{}')
    except Exception:
        return {}

def _human_bytes(n: int) -> str:
    if not n or n < 0:
        return "0B"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while n >= 1024 and i < len(units) - 1:
        n /= 1024.0
        i += 1
    return f"{n:.2f}{units[i]}"

def _human_time(seconds: float) -> str:
    if not seconds or seconds <= 0:
        return "0s"
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h {m}m {s}s"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"

def extract_media_summary(path: str) -> dict:
    info = probe_media(path)
    if not info:
        size = os.path.getsize(path) if os.path.exists(path) else 0
        return {
            "path": path,
            "container": os.path.splitext(path)[1].lstrip('.').lower(),
            "size_bytes": size,
            "size_human": _human_bytes(size),
            "duration": None,
            "duration_human": "Unknown",
            "video_codec": None,
            "audio_codec": None,
            "width": None,
            "height": None,
            "bitrate_kbps": None
        }

    format_info = info.get("format", {})
    streams = info.get("streams", [])
    v_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    a_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

    duration = None
    try:
        duration = float(format_info.get("duration")) if format_info.get("duration") else None
    except Exception:
        duration = None

    bit_rate = None
    try:
        bit_rate = int(format_info.get("bit_rate")) if format_info.get("bit_rate") else None
    except Exception:
        bit_rate = None

    size = None
    try:
        size = int(format_info.get("size")) if format_info.get("size") else (os.path.getsize(path) if os.path.exists(path) else 0)
    except Exception:
        size = os.path.getsize(path) if os.path.exists(path) else 0

    return {
        "path": path,
        "container": format_info.get("format_name") or os.path.splitext(path)[1].lstrip('.').lower(),
        "size_bytes": size,
        "size_human": _human_bytes(size),
        "duration": duration,
        "duration_human": _human_time(duration) if duration else "Unknown",
        "video_codec": v_stream.get("codec_name") if v_stream else None,
        "audio_codec": a_stream.get("codec_name") if a_stream else None,
        "width": v_stream.get("width") if v_stream else None,
        "height": v_stream.get("height") if v_stream else None,
        "bitrate_kbps": int(bit_rate / 1000) if bit_rate else None
    }

def format_media_summary(summary: dict) -> str:
    if not summary:
        return "No media info."
    parts = []
    parts.append("🧾 Media Info")
    parts.append("────────────")
    parts.append(f"File: {os.path.basename(summary.get('path', ''))}")
    if summary.get("container"):
        parts.append(f"Container: {summary['container']}")
    wh = summary.get("width"), summary.get("height")
    if wh[0] and wh[1]:
        parts.append(f"Resolution: {wh[0]}x{wh[1]}")
    if summary.get("video_codec"):
        parts.append(f"Video Codec: {summary['video_codec'].upper()}")
    if summary.get("audio_codec"):
        parts.append(f"Audio Codec: {summary['audio_codec'].upper()}")
    if summary.get("bitrate_kbps"):
        parts.append(f"Bitrate: {summary['bitrate_kbps']} kbps")
    parts.append(f"Duration: {summary['duration_human']}")
    parts.append(f"Size: {summary['size_human']}")
    return "\n".join(parts)