# plugins/sudo.py

from pyrogram import Client, filters
from pyrogram.types import Message
from Config import Config
from Bot import bot
from Database import add_sudo, remove_sudo, get_sudo_list
from Decorators import owner_only

@bot.on_message(filters.command("addsudo") & owner_only)
async def add_sudo_user(c: Client, m: Message):
    if not m.reply_to_message:
        return await m.reply("Reply to a user to add as Sudo.")
    user_id = m.reply_to_message.from_user.id
    await add_sudo(user_id)
    await m.reply(f"✅ Added `{user_id}` to Sudo Users.")

@bot.on_message(filters.command("remsudo") & owner_only)
async def remove_sudo_user(c: Client, m: Message):
    if not m.reply_to_message:
        return await m.reply("Reply to a user to remove from Sudo.")
    user_id = m.reply_to_message.from_user.id
    await remove_sudo(user_id)
    await m.reply(f"❌ Removed `{user_id}` from Sudo Users.")

@bot.on_message(filters.command("sudolist") & owner_only)
async def sudo_list(c: Client, m: Message):
    sudoers = await get_sudo_list()
    if not sudoers:
        return await m.reply("No Sudo Users added.")
    msg = "**🔰 Sudo Users List:**\n"
    msg += "\n".join([f"- `{x}`" for x in sudoers])
    await m.reply(msg)
  
