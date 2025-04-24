from pyrogram import Client, filters 
import os from config import API_ID, API_HASH, BOT_TOKEN

app = Client( "auto-subtitle-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins=dict(root="bot/plugins") )

if name == "main":
  os.makedirs("downloads", exist_ok=True)
  app.run()
