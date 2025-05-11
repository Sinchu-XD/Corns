from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Bot import bot
from Config import Config
from Decorators import subscription_required, check_subscription
from Database import get_channels, get_sudo_list
from datetime import datetime

# ✅ Async function to check if user is admin or sudo
async def is_admin(uid: int) -> bool:
    sudo_users = await get_sudo_list()
    return uid == Config.OWNER_ID or uid in sudo_users

@bot.on_message(filters.command("start") & filters.private)
@subscription_required
async def start_command(client, message: Message):
    user_id = message.from_user.id
    channels = await get_channels()

    if await is_admin(user_id):
        if isinstance(channels, dict) and len(channels) < 2:
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
        keyboard = []
        if isinstance(channels, dict):
            for slot, username in channels.items():
                keyboard.append([InlineKeyboardButton(f"📡 Join @{username}", url=f"https://t.me/{username}")])
        elif isinstance(channels, list):
            for username in channels:
                keyboard.append([InlineKeyboardButton(f"📡 Join @{username}", url=f"https://t.me/{username}")])
        else:
            return await message.reply("❌ Invalid channels format. Please contact admin.")

        # ✅ Add "I Joined" button
        keyboard.append([InlineKeyboardButton("✅ I Joined", callback_data="check_join")])

        return await message.reply(
            "📥 To access the content, please join all our channels:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        return await message.reply("❌ No channels are configured yet. Please try again later.")

@bot.on_callback_query(filters.regex("check_join"))
async def recheck_subscription(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if await check_subscription(client, user_id):
        await callback_query.message.edit("✅ You're successfully verified! You can now use the bot.")
    else:
        await callback_query.answer("🚫 You haven't joined all channels yet.", show_alert=True)
