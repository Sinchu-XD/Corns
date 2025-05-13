from telethon import TelegramClient
from Config import Config

client = TelegramClient(
    "RichFeatureBot", 
    Config.API_ID,
    Config.API_HASH
).start(bot_token=Config.BOT_TOKEN)
