from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Bot import bot
from Config import Config
from Decorators import subscription_required
from Database import get_channels
from datetime import datetime

@bot.on_message(filters.private & filters.command("start"))
@subscription_required
async def start(client, message):
    user_id = message.from_user.id
    not_joined = []
    channels = await get_channels()

    for channel in channels:
        try:
            member = await client.get_chat_member(f"@{channel}", user_id)  # Prefix with '@' here for checking membership
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(channel)
        except:
            not_joined.append(channel)

    if not_joined:
        buttons = [
            [InlineKeyboardButton(f"📢 Join @{ch}", url=f"https://t.me/{ch}")]  # Use '@' for the button URL
            for ch in not_joined
        ]
        buttons.append([InlineKeyboardButton("✅ I've Joined", callback_data="check_join")])
        await message.reply("🚫 You must join all channels to use this bot:", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply("✅ You have joined all required channels!")

# Callback check
@bot.on_callback_query(filters.regex("check_join"))
async def check_join(client, callback_query):
    user_id = callback_query.from_user.id
    not_joined = []
    channels = await get_channels()

    for channel in channels:
        try:
            member = await client.get_chat_member(f"@{channel}", user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(channel)
        except:
            not_joined.append(channel)

    if not_joined:
        await callback_query.answer("❌ Still missing some channels!", show_alert=True)
    else:
        await callback_query.message.edit("✅ You have joined all required channels!")
