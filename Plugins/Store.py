from telethon import events
from Bot import bot
from Database import save_file  # You should have this function
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto

@bot.on(events.NewMessage(func=lambda e: e.media))
async def handle_file(event):
    user = await event.get_sender()

    media = event.media

    if isinstance(media, MessageMediaDocument):
        file_type = "document"
    elif isinstance(media, MessageMediaPhoto):
        file_type = "photo"
    else:
        file_type = "unknown"

    # ✅ Save chat_id and message_id (used to forward later)
    file_info = {
        "chat_id": event.chat_id,
        "message_id": event.id,
        "file_type": file_type,
        "uploaded_by": user.id,
    }

    file_ref_id = await save_file(file_info)

    await event.reply(
        f"✅ File saved!\n\n"
        f"🔗 Share this link to retrieve:\n"
        f"`/start {file_ref_id}`",
        parse_mode="md"
    )
