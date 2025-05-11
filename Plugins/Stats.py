# plugins/stats.py

from pyrogram import Client, filters
from pyrogram.types import Message
from Main import bot
from Database import db, get_sudo_list
from Config import Config

@bot.on_message(filters.command("stats") & filters.private)
async def stats_handler(client: Client, message: Message):
    user_id = message.from_user.id
    sudoers = await get_sudo_list()
    if user_id not in sudoers and user_id != Config.OWNER_ID:
        return await message.reply("❌ You are not authorized to view stats.")

    total_files = await db.files.count_documents({})
    total_users = await db.files.distinct("user_id")
    await message.reply(
        f"📊 **Bot Stats**\n\n"
        f"👥 Total Users: `{len(total_users)}`\n"
        f"📁 Total Files: `{total_files}`"
    )
  
