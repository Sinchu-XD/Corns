from pymongo import MongoClient
import os
from Config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client["file_store_bot"]

files_collection = db["files"]
users_collection = db["users"]
sudo_users_collection = db["sudo_users"]
channels_collection = db["channels"]
settings_collection = db["settings"]

def add_file(file_id, file_name, user_id):
    files_collection.insert_one({"file_id": file_id, "file_name": file_name, "user_id": user_id})

def get_file(file_id):
    return files_collection.find_one({"file_id": file_id})

def add_user(user_id):
    users_collection.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

def add_sudo_user(user_id):
    sudo_users_collection.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

def remove_sudo_user(user_id):
    sudo_users_collection.delete_one({"user_id": user_id})

def get_sudo_users():
    return [user["user_id"] for user in sudo_users_collection.find()]

def add_channel(slot, username):
    channels_collection.update_one({"slot": slot}, {"$set": {"username": username}}, upsert=True)

def remove_channel(slot):
    channels_collection.delete_one({"slot": slot})

def get_all_channels():
    return {channel["slot"]: channel["username"] for channel in channels_collection.find()}

def set_force_check(value: bool):
    settings_collection.update_one({"_id": "force_check"}, {"$set": {"value": value}}, upsert=True)

def get_force_check():
    setting = settings_collection.find_one({"_id": "force_check"})
    return setting["value"] if setting else False
  
