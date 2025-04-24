from pyrogram import Client
import os
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "auto-subtitle-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    app.run()
