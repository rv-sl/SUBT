import os
from pyrogram.types import Message
from utils.progress import update_upload_progress

async def download_media(media_msg: Message, status_msg: Message):
    try:
        file = await media_msg.download(
            file_name="downloads/",
            progress=update_upload_progress,
            progress_args=(status_msg, "Download")
        )
        return file
    except Exception:
        return None
