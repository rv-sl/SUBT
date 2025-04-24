from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("start") & filters.private)
async def start_command(bot, message: Message):
    await message.reply(
        "**Hey!**\nI'm your FFmpeg command bot.\n\n"
        "**Commands:**\n"
        "`/ffm` - Run FFmpeg on replied media\n"
        "`/ffm your_command` - Run custom FFmpeg command on media\n\n"
        "Just reply to a video/audio file!"
    )
