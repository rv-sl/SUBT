from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import *
from utils.whisperer import generate_subtitles
from utils.translator import translate_srt
from utils.cleaner import cleanup_files
from utils.progress import progress_hook

import asyncio
import os
import time

LANGUAGES = {
    "English": "en",
    "සිංහල": "si"
}

@app.on_message(filters.command("sub") & filters.reply)
async def sub_handler(client: Client, message: Message):
    if not message.reply_to_message.video:
        return await message.reply("Please reply to a video.")

    buttons = [
        [InlineKeyboardButton(text=lang, callback_data=f"lang:{code}:{message.reply_to_message.message_id}")]
        for lang, code in LANGUAGES.items()
    ]
    await message.reply("Select subtitle language:", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex(r"lang:(.*?):(\d+)"))
async def language_selected(client, callback_query):
    lang_code, msg_id = callback_query.data.split(":")[1:]
    msg = await client.get_messages(callback_query.message.chat.id, int(msg_id))

    if not msg or not msg.video:
        return await callback_query.answer("Video not found.")

    status = await callback_query.message.edit_text("Downloading video...")
    download_path = f"downloads/{msg.video.file_id}.mp4"
    await msg.download(file_name=download_path, progress=progress_hook, progress_args=(callback_query.message, "Downloading"))

    await callback_query.message.edit_text("Generating English subtitles...")
    srt_path = await generate_subtitles(download_path, callback_query.message)

    if lang_code != "en":
        await callback_query.message.edit_text("Translating to Sinhala...")
        srt_path = await translate_srt(srt_path, lang_code)

    await callback_query.message.edit_text("Uploading subtitle file...")
    await client.send_document(callback_query.message.chat.id, srt_path, caption="Here is your subtitle.")
    await callback_query.message.delete()

    await cleanup_files(download_path, srt_path)
