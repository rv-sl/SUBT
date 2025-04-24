import time
from pyrogram.types import Message

progress_messages = {}

async def update_ffmpeg_progress(msg: Message, stage: str, line: str):
    if "time=" in line:
        parts = line.split()
        time_str = next((x for x in parts if x.startswith("time=")), None)
        speed_str = next((x for x in parts if x.startswith("speed=")), None)
        if time_str and speed_str:
            text = f"**{stage} Progress**\n`{time_str}` | `{speed_str}`"
            await throttled_edit(msg, text)

async def update_upload_progress(current, total, msg: Message, stage: str):
    percent = current * 100 // total
    text = f"**{stage}**\nUploaded: `{current // (1024*1024)}MB` / `{total // (1024*1024)}MB`\n**{percent}%**"
    await throttled_edit(msg, text)

async def throttled_edit(msg: Message, text: str):
    now = time.time()
    last = progress_messages.get(msg.chat.id, 0)
    if now - last >= 10:
        progress_messages[msg.chat.id] = now
        try:
            await msg.edit(text)
        except Exception:
            pass
