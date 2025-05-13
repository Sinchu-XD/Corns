from telethon import events
from Database import save_file  # Your DB logic to store chat_id + message_id
from Config import Config
from Bot import bot
from Decorators import owner_or_sudo

@bot.on(events.NewMessage(func=owner_or_sudo))
async def handle_file(event):
    # ✅ Only allow in private chat
    if not event.is_private:
        return await event.reply("❌ This command can only be used in private chats.")

    # ✅ Check for media (Telethon doesn't use .photo/.video like Bot API)
    if not event.media:
        return await event.reply("❌ Please send a photo, video, or document.")

    # ✅ Detect file type
    media_type = event.media
    if hasattr(media_type, 'document'):
        file_type = "document"
    elif hasattr(media_type, 'photo'):
        file_type = "photo"
    else:
        file_type = "media"

    # ✅ Save file metadata using chat_id + message_id (not file_id)
    file_info = {
        "chat_id": event.chat_id,
        "message_id": event.id,
        "file_type": file_type,
        "uploaded_by": event.sender_id,
    }

    # ✅ save_file should return a unique reference ID (Mongo ID or UUID)
    file_ref_id = await save_file(file_info)

    # ✅ Link format
    link = f"https://t.me/{Config.BOT_USERNAME}?start={file_ref_id}"

    # ✅ Confirm to user
    await event.reply(
        f"✅ File saved!\n\n🔗 **Here's your link:**\n`{link}`\n🆔 **File Ref ID:** `{file_ref_id}`",
        parse_mode="md"
    )

    # ✅ Log upload
    try:
        # Get user mention manually
        sender = await event.get_sender()
        mention = f"[{sender.first_name}](tg://user?id={sender.id})"

        await bot.send_message(
            Config.LOG_CHANNEL_ID,
            f"#UPLOAD\n👤 **Uploader:** {mention}\n"
            f"📦 **Type:** {file_type}\n🆔 **File Ref ID:** `{file_ref_id}`\n🔗 [Open File Link]({link})",
            parse_mode="md"
        )
    except Exception as e:
        print(f"[LOG ERROR] Failed to log upload: {e}")
