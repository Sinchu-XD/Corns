# plugins/delfile.py

from pyrogram import Client, filters
from pyrogram.types import Message
from Database import files_col, get_sudo_list
from Config import Config
from bson import ObjectId
from Bot import bot
from bson.errors import InvalidId

@bot.on_message(filters.command("delfile") & filters.private)
async def delete_file_handler(client: Client, message: Message):
    user_id = message.from_user.id
    sudoers = await get_sudo_list()
    if user_id not in sudoers and user_id != Config.OWNER_ID:
        return await message.reply("❌ You don't have permission to use this command.")

    if len(message.command) < 2:
        return await message.reply("Usage:\n`/delfile <file_id>`", quote=True)

    file_id = message.text.split(None, 1)[1]

    try:
        result = await files_col.delete_one({"_id": ObjectId(file_id)})
        if result.deleted_count:
            return await message.reply("✅ File deleted successfully.")
        else:
            return await message.reply("❌ No file found with that ID.")
    except InvalidId:
        return await message.reply("❌ Invalid file ID format.")
      
