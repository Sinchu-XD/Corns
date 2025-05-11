# plugins/file.py

from pyrogram import Client, filters
from pyrogram.types import Message
from Database import save_file
from Bot import bot
from Config import Config
from Decorators import owner_or_sudo
@bot.on_message(filters.private & filters.media & owner_or_sudo)
async def handle_file(c: Client, m: Message):
    media = m.photo or m.video or m.document
    if not media:
        return await m.reply("Send a photo, video, or document.")
    
    file_type = (
        "photo" if m.photo else
        "video" if m.video else
        "document"
    )
    
    file_id = media.file_id
    file_ref_id = await save_file(m.from_user.id, file_id, file_type)

    link = f"https://t.me/{Config.BOT_USERNAME}?start={file_ref_id}"
    await m.reply(
        f"✅ File saved!\n🔗 **Here’s your link:**\n`{link}`\n🆔 File ID: `{file_ref_id}`",
        quote=True
    )
  
