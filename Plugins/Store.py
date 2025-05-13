from telethon import TelegramClient, events
from Database import save_file
from Config import Config
from Bot import bot
from Decorators import owner_or_sudo

@bot.on(events.NewMessage(pattern=None, func=owner_or_sudo))
async def handle_file(event):
    # Check if the message is from a private chat
    if not event.is_private:
        return await event.reply("This command can only be used in private chats.")

    # Check if the message contains media (photo, video, document)
    media = event.photo or event.video or event.document
    if not media:
        return await event.reply("Send a photo, video, or document.")
    
    # Determine the file type (photo, video, or document)
    file_type = (
        "photo" if event.photo else
        "video" if event.video else
        "document"
    )
    
    # Save the file
    file_id = media.file_id
    file_ref_id = await save_file(event.sender_id, file_id, file_type)

    # Generate the link for the file
    link = f"https://t.me/{Config.BOT_USERNAME}?start={file_ref_id}"
    
    # Reply with the link
    await event.reply(
        f"✅ File saved!\n🔗 **Here’s your link:**\n`{link}`\n🆔 File ID: `{file_ref_id}`",
        quote=True
    )

    # Log the file upload to the log channel
    try:
        await bot.send_message(
            Config.LOG_CHANNEL_ID,
            f"#UPLOAD\n👤 **Uploader:** {event.sender.mention}\n"
            f"📦 **Type:** {file_type}\n🆔 **File Ref ID:** `{file_ref_id}`\n🔗 [Open File Link]({link})"
        )
    except Exception as e:
        print(f"[LOG ERROR] Failed to log upload: {e}")
