from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Bot import bot
from Config import Config
from Database import get_file_by_id, get_channels, get_main_channel
from bson.errors import InvalidId
from Decorators import check_subscription
import asyncio


# ✅ /start restore command
@bot.on_message(filters.command("start") & filters.private & filters.regex(r"^/start\s(.+)"))
async def start_link_restore(c: Client, m: Message):
    user_id = m.from_user.id
    file_ref_id = m.text.split(" ", 1)[1]

    # ✅ Check if user joined required channels
    if not await check_subscription(c, user_id):
        channels = await get_channels()
        buttons = [
            [InlineKeyboardButton(f"📡 Join @{ch}", url=f"https://t.me/{ch}")]
            for ch in channels.values()
        ]
        buttons.append([InlineKeyboardButton("✅ I Joined", callback_data=f"check_join_restore|{file_ref_id}")])

        return await m.reply(
            "🚫 To access the file, please join all the required channels:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # ✅ Proceed with file restore
    try:
        data = await get_file_by_id(file_ref_id)
    except InvalidId:
        return await m.reply("❌ Invalid or expired file link.")

    if not data:
        return await m.reply("❌ File not found or deleted.")

    try:
        await bot.send_message(
            Config.LOG_CHANNEL_ID,
            f"#RESTORE\n👤 **User:** {m.from_user.mention}\n"
            f"📁 **Requested File ID:** `{file_ref_id}`\n📦 **Type:** {data['file_type']}"
        )
    except Exception as e:
        print(f"[LOG ERROR] {e}")

    info_msg = await m.reply(
        f"**📂 Sending your {data['file_type']}...**\n\nThis file will auto-delete in 20 minutes."
    )

    sent = await c.send_cached_media(m.chat.id, data["file_id"])

    await asyncio.sleep(1200)  # 20 minutes
    try:
        await sent.delete()
        await info_msg.delete()
    except Exception as e:
        print(f"[AUTO DELETE ERROR] {e}")


# ✅ Callback recheck for restore
@bot.on_callback_query(filters.regex(r"check_join_restore\|(.+)"))
async def recheck_restore_join(c: Client, cb: CallbackQuery):
    user_id = cb.from_user.id
    file_ref_id = cb.data.split("|")[1]

    if not await check_subscription(c, user_id):
        return await cb.answer("🚫 You haven't joined all channels yet.", show_alert=True)

    await cb.message.delete()
    fake_msg = cb.message
    fake_msg.text = f"/start {file_ref_id}"
    await start_link_restore(c, fake_msg)
