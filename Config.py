import os

API_ID = int(os.getenv("API_ID", 6067591))
API_HASH = os.getenv("API_HASH", "94e17044c2393f43fda31d3afe77b26b")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7849290437:AAGsPd0m4de-bcNXYNvqb8fgBQ5eNHXyc2Q")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://Sinchu:Sinchu@sinchu.qwijj.mongodb.net/?retryWrites=true&w=majority&appName=Sinchu")

OWNER_ID = int(os.getenv("OWNER_ID", 8091116698, 7862043458))
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", -1002287107269))

SUDO_USERS = [OWNER_ID]  # Extendable via /addsudo
