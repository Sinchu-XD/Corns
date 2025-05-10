# Telegram @Itz_Your_4Bhi
# Copyright ©️ 2025

from pymongo import MongoClient
from Config import Config

client = MongoClient(Config.MONGO_URI)
db = client["RichBot"]

# Collections
channels_db = db["channels"]
sudos_db = db["sudos"]
files_db = db["files"]

# CHANNELS
def add_channel(channel_id):
    if not channels_db.find_one({"channel_id": channel_id}):
        channels_db.insert_one({"channel_id": channel_id})

def remove_channel(channel_id):
    channels_db.delete_one({"channel_id": channel_id})

def get_all_channels():
    return [ch["channel_id"] for ch in channels_db.find()]

def channels_exist():
    return channels_db.count_documents({}) > 0

# SUDO USERS
def add_sudo(user_id):
    if not sudos_db.find_one({"user_id": user_id}):
        sudos_db.insert_one({"user_id": user_id})

def remove_sudo(user_id):
    sudos_db.delete_one({"user_id": user_id})

def get_sudo_users():
    return [s["user_id"] for s in sudos_db.find()]

def is_sudo(user_id):
    return user_id == Config.OWNER_ID or sudos_db.find_one({"user_id": user_id}) is not None

# FILE STORAGE
def save_file(file_id, user_id, link):
    files_db.insert_one({"user_id": user_id, "file_id": file_id, "link": link})

def get_user_files(user_id):
    return files_db.find({"user_id": user_id})

def set_main_channel(channel: str):
    db.config.update_one({"_id": "main_channel"}, {"$set": {"channel": channel}}, upsert=True)

def get_main_channel():
    doc = db.config.find_one({"_id": "main_channel"})
    return doc["channel"] if doc else None
