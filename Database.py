from pymongo import MongoClient
from Config import MONGO_URL

# Initialize MongoDB client and collections
client = MongoClient(MONGO_URL)
db = client["file_store_bot"]

files_collection = db["files"]
users_collection = db["users"]
sudo_users_collection = db["sudo_users"]
channels_collection = db["channels"]
settings_collection = db["settings"]

# ➤ Save a file's metadata
def add_file(file_id: str, file_name: str, user_id: int):
    try:
        files_collection.update_one(
            {"file_id": file_id},
            {"$set": {"file_name": file_name, "user_id": user_id}},
            upsert=True
        )
    except Exception as e:
        print(f"Error adding file: {e}")

# ➤ Retrieve file metadata by file_id
def get_file(file_id: str):
    try:
        return files_collection.find_one({"file_id": file_id})
    except Exception as e:
        print(f"Error retrieving file: {e}")
        return None

# ➤ Add or update a user
def add_user(user_id: int):
    try:
        users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id}},
            upsert=True
        )
    except Exception as e:
        print(f"Error adding user: {e}")

# ➤ Sudo Users
def add_sudo_user(user_id: int):
    try:
        sudo_users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id}},
            upsert=True
        )
    except Exception as e:
        print(f"Error adding sudo user: {e}")

def remove_sudo_user(user_id: int):
    try:
        sudo_users_collection.delete_one({"user_id": user_id})
    except Exception as e:
        print(f"Error removing sudo user: {e}")

def get_sudo_users():
    try:
        return [user["user_id"] for user in sudo_users_collection.find()]
    except Exception as e:
        print(f"Error fetching sudo users: {e}")
        return []

# ➤ Channels
def add_channel(slot: str, username: str):
    try:
        channels_collection.update_one(
            {"slot": slot},
            {"$set": {"username": username}},
            upsert=True
        )
    except Exception as e:
        print(f"Error adding channel: {e}")

def remove_channel(slot: str):
    try:
        channels_collection.delete_one({"slot": slot})
    except Exception as e:
        print(f"Error removing channel: {e}")

def get_all_channels():
    try:
        return {channel["slot"]: channel["username"] for channel in channels_collection.find()}
    except Exception as e:
        print(f"Error fetching channels: {e}")
        return {}

# ➤ Force Check Setting
def set_force_check(value: bool):
    try:
        settings_collection.update_one(
            {"_id": "force_check"},
            {"$set": {"value": value}},
            upsert=True
        )
    except Exception as e:
        print(f"Error setting force_check: {e}")

def get_force_check():
    try:
        setting = settings_collection.find_one({"_id": "force_check"})
        return setting["value"] if setting else False
    except Exception as e:
        print(f"Error getting force_check: {e}")
        return False
