# plugins/restore.py

from pyrogram import Client, filters
from pyrogram.types import Message
from Bot import bot
from Database import get_file_by_id
from bson.errors import InvalidId

@bot.on_message(filters.command("start") & filters.private & filters.regex(r"^/start\s(.+)"))
async def start_link_restore(c: Client, m: Message):
    file_ref_id = m.text.split(" ", 1)[1]
    try:
        data = await get_file_by_id(file_ref_id)
    except InvalidId:
        return await m.reply("❌ Invalid or expired file link.")

    if not data:
        return await m.reply("❌ File not found or deleted.")

    await m.reply(
        f"📂 Sending your saved {data['file_type']}...",
        quote=True
    )
    await c.send_cached_media(m.chat.id, data["file_id"])
  
