from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Bot import bot
from Config import Config
from Decorators import subscription_required, check_subscription
from Database import get_file_by_id, get_channels
from bson.errors import InvalidId
import asyncio


# ✅ Function to check if user is a member of a given channel
async def is_member(client: Client, user_id: int, channel: str) -> bool:
    try:
        chat = await client.get_chat(channel)
        member = await client.get_chat_member(chat.id, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"[JOIN CHECK ERROR] Channel: {channel} — {e}")
        return False


@bot.on_message(filters.command("start") & filters.private & filters.regex(r"^/start\s(.+)"))
@subscription_required
async def start_link_restore(c: Client, m: Message):
    user_id = m.from_user.id
    file_ref_id = m.text.split(" ", 1)[1]

    # ✅ Get required channels from DB
    try:
        channels = await get_channels()
    except Exception as e:
        print(f"[DB ERROR] Failed to get channels: {e}")
        return await m.reply("⚠️ Internal error while fetching channel data.")

    not_joined = []

    if isinstance(channels, dict):
        for ch in channels.values():
            if not await is_member(c, user_id, ch):
                not_joined.append(ch)
    elif isinstance(channels, list):
        for ch in channels:
            if not await is_member(c, user_id, ch):
                not_joined.append(ch)
    else:
        return await m.reply("⚠️ Invalid channel data format in database.")

    if not_joined:
        buttons = [[InlineKeyboardButton(f"📡 Join @{ch}", url=f"https://t.me/{ch}")] for ch in not_joined]
        buttons.append([InlineKeyboardButton("✅ I Joined", callback_data=f"check_join_restore|{file_ref_id}")])
        return await m.reply(
            "🚫 To access the file, please join the required channels first:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # ✅ Proceed with file restore
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
            f"#RESTORE\n👤 **User:** {m.from_user.mention}\n"
            f"📁 **Requested File ID:** `{file_ref_id}`\n📦 **Type:** {data['file_type']}"
        )
    except Exception as e:
        print(f"[LOG ERROR] Failed to log restore: {e}")

    info_msg = await m.reply(
        f"**📂 Sending your {data['file_type']}...**\n\nThis {data['file_type']} will auto-delete in 20 minutes.",
        quote=True
    )

    # ⬇️ Handling file sending based on the type
    try:
        if data['file_type'] == 'photo':  # Send photo
            sent = await c.send_photo(m.chat.id, data["file_id"])
        elif data['file_type'] == 'video':  # Send video
            sent = await c.send_video(m.chat.id, data["file_id"])
        else:  # Default to sending as document (works for all file types)
            sent = await c.send_document(m.chat.id, data["file_id"])
    except Exception as e:
        return await m.reply(f"❌ Failed to send media: {e}")

    # ⏳ Auto-delete after 20 minutes
    await asyncio.sleep(1200)
    try:
        await sent.delete()
        await info_msg.delete()
    except Exception as e:
        print(f"[AUTO DELETE ERROR] {e}")



@bot.on_callback_query(filters.regex("check_join_restore"))
async def recheck_subscription(client: Client, cb: CallbackQuery):
    user_id = cb.from_user.id
    file_ref_id = cb.data.split("|")[1]

    # ✅ Check if user has joined all channels
    if not await check_subscription(client, user_id):
        await cb.answer("🚫 You haven't joined all required channels yet.", show_alert=True)
        return  # 🔁 Do not continue to restore flow if not joined

    await cb.answer("✅ You're successfully verified!", show_alert=True)
    await cb.message.delete()

    # ✅ Trigger file restore as a simulated command
    fake_message = cb.message
    fake_message.text = f"/start {file_ref_id}"
    fake_message.from_user.id = user_id  # Make sure ID is preserved
    await start_link_restore(client, fake_message)
