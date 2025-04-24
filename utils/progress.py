import time

progress_records = {}

async def progress_hook(current, total, message, label="Progress"):
    now = time.time()
    last = progress_records.get(message.chat.id, 0)
    if now - last > 10:
        percent = round((current / total) * 100, 2)
        await message.edit_text(f"{label}: {percent}%\nDownloaded: {current / 1024 ** 2:.2f}MB / {total / 1024 ** 2:.2f}MB")
        progress_records[message.chat.id] = now

async def update_ffmpeg_progress(message, stage, line):
    now = time.time()
    last = progress_records.get(message.chat.id, 0)
    if now - last > 10:
        await message.edit_text(f"{stage} Progress:\n{line}")
        progress_records[message.chat.id] = now
