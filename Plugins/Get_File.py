from pyrogram import Client, filters
from pyrogram.types import Message
from Bot import bot
from Database import get_file_by_id
from Config import Config
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

    # ✅ Log restore activity
    try:
        await bot.send_message(
            Config.LOG_CHANNEL_ID,
            f"#RESTORE\n👤 **User:** {message.from_user.mention}\n"
            f"📁 **Requested File ID:** `{file_ref_id}`\n📦 **Type:** {data['file_type']}"
        )
    except Exception as e:
        print(f"[LOG ERROR] Failed to log restore: {e}")

    await m.reply(f"**📂 Sending your Video{data['file_type']}...**", quote=True)
    await c.send_cached_media(m.chat.id, data["file_id"])
