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

# Add a file to the database
def add_file(file_id, file_name, user_id):
    try:
        files_collection.insert_one({"file_id": file_id, "file_name": file_name, "user_id": user_id})
        print(f"File {file_name} added successfully to the database.")
    except Exception as e:
        print(f"Error adding file to database: {e}")

# Get file details by file_id
def get_file(file_id):
    try:
        file = files_collection.find_one({"file_id": file_id})
        return file
    except Exception as e:
        print(f"Error fetching file from database: {e}")
        return None

# Add a user to the users collection
def add_user(user_id):
    try:
        users_collection.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
        print(f"User {user_id} added/updated in the database.")
    except Exception as e:
        print(f"Error adding user to database: {e}")

# Add a sudo user to the sudo_users collection
def add_sudo_user(user_id):
    try:
        sudo_users_collection.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
        print(f"Sudo user {user_id} added/updated.")
    except Exception as e:
        print(f"Error adding sudo user to database: {e}")

# Remove a sudo user from the sudo_users collection
def remove_sudo_user(user_id):
    try:
        sudo_users_collection.delete_one({"user_id": user_id})
        print(f"Sudo user {user_id} removed.")
    except Exception as e:
        print(f"Error removing sudo user from database: {e}")

# Get all sudo users from the sudo_users collection
def get_sudo_users():
    try:
        return [user["user_id"] for user in sudo_users_collection.find()]
    except Exception as e:
        print(f"Error fetching sudo users: {e}")
        return []

# Add a channel to the channels collection
def add_channel(slot, username):
    try:
        channels_collection.update_one({"slot": slot}, {"$set": {"username": username}}, upsert=True)
        print(f"Channel {username} added/updated in slot {slot}.")
    except Exception as e:
        print(f"Error adding channel to database: {e}")

# Remove a channel from the channels collection
def remove_channel(slot):
    try:
        channels_collection.delete_one({"slot": slot})
        print(f"Channel in slot {slot} removed.")
    except Exception as e:
        print(f"Error removing channel from database: {e}")

# Get all channels from the channels collection
def get_all_channels():
    try:
        return {channel["slot"]: channel["username"] for channel in channels_collection.find()}
    except Exception as e:
        print(f"Error fetching all channels: {e}")
        return {}

# Set the force check value in the settings collection
def set_force_check(value: bool):
    try:
        settings_collection.update_one({"_id": "force_check"}, {"$set": {"value": value}}, upsert=True)
        print(f"Force check setting set to {value}.")
    except Exception as e:
        print(f"Error setting force check in database: {e}")

# Get the force check value from the settings collection
def get_force_check():
    try:
        setting = settings_collection.find_one({"_id": "force_check"})
        return setting["value"] if setting else False
    except Exception as e:
        print(f"Error fetching force check setting: {e}")
        return False
