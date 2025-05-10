# Plugins/start.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Config import Config
from Database import get_all_channels, channels_exist, is_sudo, get_main_channel
from pyrogram.errors import UserNotParticipant

LOG_CHANNEL = Config.LOG_CHANNEL_ID

# Build join buttons
def build_join_buttons(channels):
    buttons = []
    for ch in channels:
        buttons.append([InlineKeyboardButton("🔗 Join", url=f"https://t.me/" + ch.replace("@", ""))])
    buttons.append([InlineKeyboardButton("✅ I've Joined", callback_data="check_join")])
    return InlineKeyboardMarkup(buttons)

@Client.on_message(filters.command("start") & filters.private)
async def start(bot, message: Message):
    user = message.from_user
    uid = user.id

    # Log start
    try:
        await bot.send_message(LOG_CHANNEL, f"👤 [{user.first_name}](tg://user?id={uid}) (`{uid}`) used /start")
    except:
        pass

    # Are channels added?
    channels = get_all_channels()
    if not channels:
        return await message.reply("⚠️ No channels configured. Please ask the owner to /addchannel first.")

    # Check if user joined all channels
    not_joined = []
    for ch in channels:
        try:
            await bot.get_chat_member(ch, uid)
        except UserNotParticipant:
            not_joined.append(ch)

    if not_joined:
        return await message.reply(
            "📛 Please join all channels to use this bot.",
            reply_markup=build_join_buttons(not_joined)
        )

    # If joined all → show message based on role
    if is_sudo(uid):
        await message.reply(
            "✅ All channels joined!\n\n🔐 You are authorized. Send me a photo, video or document to get a sharable link."
        )
    else:
        await message.reply("✅ All channels joined!\n\nThanks.")
        main_channel = get_main_channel()
        if main_channel:
            await message.reply(
                "👇 Visit Our Main Channel",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("📢 Main Channel", url=f"https://t.me/{main_channel.replace('@','')}")]]
                )
            )

@Client.on_callback_query(filters.regex("check_join"))
async def check_joined(bot, callback):
    uid = callback.from_user.id
    channels = get_all_channels()
    not_joined = []

    for ch in channels:
        try:
            await bot.get_chat_member(ch, uid)
        except UserNotParticipant:
            not_joined.append(ch)

    if not_joined:
        await callback.answer("❌ You still haven't joined all required channels.", show_alert=True)
    else:
        if is_sudo(uid):
            await callback.message.edit("✅ All channels joined!\n\n🔐 You can now send a file.")
        else:
            await callback.message.edit("✅ Channels joined!\n\n⚠️ But only Admins/Sudo can use this bot to upload files.")
          
