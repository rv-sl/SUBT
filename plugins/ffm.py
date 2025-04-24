import asyncio
import os
import shlex
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.progress import update_ffmpeg_progress, update_upload_progress
from downloader import download_media

# Default ffmpeg command template (can be updated via /ffm)
ffmpeg_command_template = "-i INPUT -c:v libx264 -preset fast OUTPUT"

@Client.on_message(filters.command("ffm") & filters.reply)
async def ffmpeg_handler(client: Client, message: Message):
    global ffmpeg_command_template

    # Update the FFmpeg command if provided
    if len(message.command) > 1:
        ffmpeg_command_template = message.text.split(None, 1)[1]
        await message.reply_text(
            f"Updated FFmpeg command to:\n`{ffmpeg_command_template}`", parse_mode="markdown"
        )
        return

    media = message.reply_to_message
    if not any([media.video, media.audio, media.document]):
        await message.reply("Please reply to a video, audio, or document file.")
        return

    status_msg = await message.reply("**Downloading file...**")
    input_file = await download_media(media, status_msg)
    if not input_file:
        await status_msg.edit("Download failed.")
        return

    input_path = os.path.abspath(input_file)
    output_path = os.path.join("downloads", f"converted_{os.path.basename(input_file)}")

    # Build the ffmpeg command
    ffmpeg_cmd = ffmpeg_command_template.replace("INPUT", shlex.quote(input_path)).replace("OUTPUT", shlex.quote(output_path))
    args = ["ffmpeg"] + shlex.split(ffmpeg_cmd)

    await status_msg.edit("**Processing file with FFmpeg...**")
    process = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    while True:
        line = await process.stderr.readline()
        if not line:
            break
        await update_ffmpeg_progress(status_msg, "FFmpeg", line.decode().strip())
    await process.wait()

    if not os.path.exists(output_path):
        await status_msg.edit("FFmpeg failed to produce output.")
        return

    await status_msg.edit("**Uploading result...**")
    await client.send_document(
        chat_id=message.chat.id,
        document=output_path,
        reply_to_message_id=message.id,
        progress=update_upload_progress,
        progress_args=(status_msg, "Upload")
    )

    # Clean up
    os.remove(input_path)
    os.remove(output_path)
    await status_msg.delete()
