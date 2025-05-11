# main.py

from pyrogram import Client
from Config import Config
import os
import asyncio
import importlib
import glob

plugin_folder = "Plugins"
for filename in os.listdir(plugin_folder):
    if filename.endswith(".py"):
        importlib.import_module(f"{plugin_folder}.{filename[:-3]}")


bot = Client(
    "RichFeatureBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
)

if __name__ == "__main__":
    print(">> Bot Starting...")
    bot.run()
    
