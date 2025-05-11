# Config.py

import os

class Config:
    API_ID = int(os.environ.get("API_ID", "YOUR_API_ID"))
    API_HASH = os.environ.get("API_HASH", "YOUR_API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")

    MONGO_URI = os.environ.get("MONGO_URI", "YOUR_MONGODB_URI")
    OWNER_ID = int(os.environ.get("OWNER_ID", "123456789"))  # Your Telegram user ID

    LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", "-100XXXXXXXXXX"))  # Logs group/channel ID
    BOT_USERNAME = "CornHub69Bot"
