from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Bot import bot
from Config import Config
from Decorators import subscription_required
from Database import get_channels, get_sudo_list
from datetime import datetime

def is_admin(uid):
    return uid in OWNER_ID or uid in get_sudo_list()
    
@bot.on_message(filters.command("start") & filters.private)
@subscription_required
async def start_command(client, message: Message):
    user_id = message.from_user.id
    channels = get_channels()

    if is_admin(user_id):
        if len(channels) < 2:
            return await message.reply(
                "⚠️ You need to add at least **2 channels** using:\n`/addch <slot> <@channel>`"
            )
        return await message.reply(
            "👋 Welcome Admin!\n\n📤 Send any file to convert into a sharable link.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📡 View Channels", callback_data="view_channels")]]
            )
        )

    # For NON-ADMIN users
    if channels:
        keyboard = [
            [InlineKeyboardButton(f"📡 Join @{username}", url=f"https://t.me/{username}")]
            for slot, username in channels.items()
        ]
        return await message.reply(
            "📥 To access the content, please join all our channels:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        return await message.reply("❌ No channels are configured yet. Please try again later.")
