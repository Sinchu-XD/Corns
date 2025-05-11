# Telegram @Itz_Your_4Bhi
# Copyright ©️ 2025

# helpers/db.py

from Config import Config
from pymongo import MongoClient

db = MongoClient(Config.MONGO_URI).RichBot
sudo_col = db.sudo_users

async def add_sudo(user_id: int):
    if not await sudo_col.find_one({"user_id": user_id}):
        await sudo_col.insert_one({"user_id": user_id})

async def remove_sudo(user_id: int):
    await sudo_col.delete_one({"user_id": user_id})

async def get_sudo_list():
    return [x["user_id"] for x in await sudo_col.find().to_list(length=0)]

# Add below existing sudo functions in helpers/db.py

channel_col = db.required_channels

async def add_channel(username: str):
    if not await channel_col.find_one({"username": username}):
        await channel_col.insert_one({"username": username})

async def remove_channel(username: str):
    await channel_col.delete_one({"username": username})

async def get_channels():
    return [x["username"] for x in await channel_col.find().to_list(length=1000)]

files_col = db.files

async def save_file(user_id: int, file_id: str, file_type: str):
    doc = {
        "user_id": user_id,
        "file_id": file_id,
        "file_type": file_type,
        "time": datetime.utcnow()
    }
    insert = await files_col.insert_one(doc)
    return str(insert.inserted_id)

async def get_file_by_id(file_id: str):
    return await files_col.find_one({"_id": ObjectId(file_id)})
    
