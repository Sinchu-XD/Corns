# plugins/start.py

from pyrogram import Client, filters
from Bot import bot
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Config import Config
from Decorators import check_user_joined
from Database import get_channels, get_sudo_list
from Decorators import owner_or_sudo
from datetime import datetime

@bot.on_message(filters.command("start"))
async def start_bot(client: Client, message: Message):
    user_id = message.from_user.mention
    channels = await get_channels()
    sudoers = await get_sudo_list()

    # log start
    try:
        await client.send_message(
            Config.LOG_GROUP_ID,
            f"👤 User : {user_id} started the bot.\n🕒 `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        )
    except:
        pass

    # if less than 2 channels
    if len(channels) < 2:
        if user_id in sudoers or user_id == Config.OWNER_ID:
            return await message.reply("⚠️ Add at least 2 channels using `/addchannel`.")
        return await message.reply("⚠️ Bot is under setup. Ask the owner to configure channels.")

    # check if joined all
    joined = await check_user_joined(client, user_id)
    if not joined:
        buttons = [[InlineKeyboardButton("✅ Joined All", callback_data="check_join")]]
        for ch in channels:
            buttons.insert(0, [InlineKeyboardButton(f"Join {ch}", url=f"https://t.me/{ch.replace('@', '')}")])
        return await message.reply(
            "**🔒 Please join all required channels to use the bot.**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # access granted
    await message.reply(
        "✅ You're verified!\n\nNow send me a **File** (Photo, Video, or Document) to get a direct link.",
    )

from pyrogram.types import CallbackQuery

@bot.on_callback_query(filters.regex("check_join"))
async def recheck_join(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    joined = await check_user_joined(client, user_id)
    if not joined:
        return await callback_query.answer("❌ You still haven't joined all channels!", show_alert=True)

    await callback_query.message.edit("✅ You're verified!\nNow send a File to get its link.")
    
