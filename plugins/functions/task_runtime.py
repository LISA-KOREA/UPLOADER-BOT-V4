"""
In-memory task registry for download pause/resume/cancel.
For persistence across restarts, extend to write/read JSON in a .tasks directory.
This registry stores task metadata used by pause/resume/cancel callbacks.
"""
import asyncio
from typing import Dict, Any

TASKS: Dict[str, Dict[str, Any]] = {}
TASKS_LOCK = asyncio.Lock()


async def set_task(task_id: str, data: Dict[str, Any]):
    async with TASKS_LOCK:
        TASKS[task_id] = data


async def get_task(task_id: str) -> Dict[str, Any]:
    async with TASKS_LOCK:
        return TASKS.get(task_id) or {}


async def del_task(task_id: str):
    async with TASKS_LOCK:
        TASKS.pop(task_id, None)


async def list_tasks_for_user(user_id: int):
    async with TASKS_LOCK:
        return {tid: t for tid, t in TASKS.items() if t.get("user_id") == user_id}