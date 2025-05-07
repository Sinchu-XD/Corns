import os

API_ID = int(os.getenv("API_ID", 6067591))
API_HASH = os.getenv("API_HASH", "94e17044c2393f43fda31d3afe77b26b")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7849290437:AAGsPd0m4de-bcNXYNvqb8fgBQ5eNHXyc2Q")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://Sinchu:Sinchu@sinchu.qwijj.mongodb.net/?retryWrites=true&w=majority&appName=Sinchu")

# Handle multiple OWNER_IDs as a list
OWNER_IDS = os.getenv("OWNER_ID", "7862043458").split(",")
OWNER_IDS = [int(x.strip()) for x in OWNER_IDS if x.strip().isdigit()]

# Primary owner for specific logic
OWNER_ID = OWNER_IDS[0] if OWNER_IDS else None

LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", -1002287107269))

# SUDO_USERS includes all OWNER_IDS by default, plus others if set
SUDO_USERS = os.getenv("SUDO_USERS", "").split(",")
SUDO_USERS = list(set(OWNER_IDS + [int(x.strip()) for x in SUDO_USERS if x.strip().isdigit()]))

