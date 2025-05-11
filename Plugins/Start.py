# Plugins/start.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Bot import bot
from Config import Config
from Decorators import check_user_joined
from Database import get_channels, get_sudo_list
from datetime import datetime

@bot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    not_joined = []
    for channel in get_channels():
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(channel)
        except:
            not_joined.append(channel)

    if not_joined:
        buttons = [
            [InlineKeyboardButton(f"📢 Join @{ch}", url=f"https://t.me/{ch}")]
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
    for channel in get_channels():
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(channel)
        except:
            not_joined.append(channel)

    if not_joined:
        await callback_query.answer("❌ Still missing some channels!", show_alert=True)
    else:
        await callback_query.message.edit("✅ You have joined all required channels!")
