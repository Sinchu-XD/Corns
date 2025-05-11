# main.py

from pyrogram import Client
from Config import Config
import os
import asyncio
import importlib
import glob
import Plugins

bot = Client(
    "RichFeatureBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins={"root": "Plugins"}
)

if __name__ == "__main__":
    print(">> Bot Starting...")
    bot.run()
    
