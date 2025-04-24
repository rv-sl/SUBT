import subprocess
import os
from utils.progress import update_ffmpeg_progress

async def generate_subtitles(video_path, message):
    srt_path = video_path.replace(".mp4", ".srt")
    cmd = [
        "whisper",
        video_path,
        "--model", "base",
        "--language", "en",
        "--output_format", "srt",
        "--output_dir", "downloads"
    ]
    process = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = await process.stderr.readline()
        if not line:
            break
        await update_ffmpeg_progress(message, "Whisper", str(line.decode().strip()))
    await process.wait()
    return srt_path
