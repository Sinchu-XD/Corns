from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Bot import bot
from Config import Config
from Decorators import require_join, owner_or_sudo
from Decorators import send_join_prompt
from Database import get_channels, get_sudo_list
from datetime import datetime

@bot.on_message(filters.command("start") & filters.private & require_join)
async def start_bot(client: Client, message: Message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    channels = await get_channels()
    sudoers = await get_sudo_list()

    # Logging
    try:
        await bot.send_message(
            Config.LOG_GROUP_ID,
            f"👤 User : {mention} started the bot.\n🕒 `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        )
    except:
        pass

    # If channels not configured
    if not channels or len(channels) < 2:
        if user_id == Config.OWNER_ID or user_id in sudoers:
            return await message.reply("⚠️ Add at least 2 channels using `/addchannel` to make the bot functional.")
        return await message.reply("⚠️ Bot is under setup. Please wait until the owner configures it.")

    await message.reply(
        "✅ You're verified!\n\nNow send me a **File** (Photo, Video, or Document) to get a direct link."
    )


@bot.on_callback_query(filters.regex("check_join"))
async def recheck_join(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    sudoers = await get_sudo_list()
    channels = await get_channels()

    if not channels or len(channels) < 2:
        return await callback_query.message.edit_text(
            "⚠️ Bot is under setup. Required channels are not configured. Please contact the bot owner."
        )

    from helpers.check_join import check_user_joined
    joined = await check_user_joined(client, user_id)

    if not joined:
        try:
            await callback_query.answer(
                "❌ You still haven't joined all the required channels!", show_alert=True
            )
        except:
            pass
        return

    if user_id == Config.OWNER_ID or user_id in sudoers:
        await callback_query.message.edit_text(
            "✅ You're verified!\n\nNow send me a **File** (Photo, Video, or Document) to get a direct link."
        )
    else:
        await callback_query.message.edit_text("✅ **Thanks for joining us!**")
