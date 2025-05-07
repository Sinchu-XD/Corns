import os
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
from Config import API_ID, API_HASH, BOT_TOKEN, OWNER_IDS, LOG_GROUP_ID, SUDO_USERS
from Database import (
    add_file, get_file, add_user, add_sudo_user, remove_sudo_user,
    get_sudo_users, add_channel, remove_channel, get_all_channels,
    set_force_check, get_force_check
)
from Decorators import subscription_required

load_dotenv()

bot = Client("file_store_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ START command with deep link file support
@bot.on_message(filters.command("start") & filters.private)
@subscription_required
async def start_command(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS and user_id not in SUDO_USERS:
        await message.reply("👋 Hello Admin!\n\n📩 Send me any file like image, document, or video and I’ll convert it into a shareable link.")
    else:
        main_chat = get_all_channels()
        if main_chat:
            await message.reply(
                "🍿 You can get corn content here.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔗 View Content", url=main_chat)]]
                )
            )
        else:
            await message.reply("❌ No content link set by admin.")

# ✅ Save file and generate link
@bot.on_message(filters.private & (filters.document | filters.video | filters.photo))
@subscription_required
async def handle_file(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS and user_id not in SUDO_USERS:
        return await message.reply("🚫 You are not allowed to upload files.")

    media = message.document or message.video or message.photo
    file_id = media.file_id
    file_name = getattr(media, "file_name", "Unnamed File")

    add_file(file_id, file_name, user_id)

    bot_username = (await client.get_me()).username
    deep_link = f"https://t.me/{bot_username}?start={file_id}"

    await message.reply(
        f"✅ File saved as `{file_name}`.\n"
        f"🔗 [Click here to access your file]({deep_link})",
        disable_web_page_preview=True
    )

    await client.send_message(
        LOG_GROUP_ID,
        f"📥 File stored by `{user_id}`: `{file_name}`\n"
        f"🔗 [Link]({deep_link})",
        disable_web_page_preview=True
    )

# ✅ Channel management commands
@bot.on_message(filters.command("addch"))
async def add_channel_command(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS and user_id not in SUDO_USERS:
        return await message.reply("🚫 You do not have permission to add channels.")

    try:
        _, slot, username = message.text.split(maxsplit=2)
        add_channel(slot, username)
        await message.reply(f"✅ Channel {username} added in slot {slot}.")
    except ValueError:
        await message.reply("⚠️ Usage: /addch <slot> <channel_username>")

@bot.on_message(filters.command("rmch"))
async def remove_channel_command(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS and user_id not in SUDO_USERS:
        return await message.reply("🚫 You do not have permission to remove channels.")

    try:
        _, slot = message.text.split(maxsplit=1)
        remove_channel(slot)
        await message.reply(f"✅ Channel in slot {slot} removed.")
    except ValueError:
        await message.reply("⚠️ Usage: /rmch <slot>")

# ✅ SUDO management
@bot.on_message(filters.command("addsudo"))
async def add_sudo(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        return await message.reply("🚫 Only the owner can add sudo users.")

    try:
        _, target = message.text.split(maxsplit=1)
        target_user = int(target)
        add_sudo_user(target_user)
        await message.reply(f"✅ `{target_user}` added as SUDO.")
    except (ValueError, IndexError):
        await message.reply("⚠️ Usage: /addsudo <user_id>")

@bot.on_message(filters.command("rmsudo"))
async def remove_sudo(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        return await message.reply("🚫 Only the owner can remove sudo users.")

    try:
        _, target = message.text.split(maxsplit=1)
        target_user = int(target)
        remove_sudo_user(target_user)
        await message.reply(f"✅ `{target_user}` removed from SUDO.")
    except (ValueError, IndexError):
        await message.reply("⚠️ Usage: /rmsudo <user_id>")

@bot.on_message(filters.command("sudolist"))
async def show_sudo_list(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        return await message.reply("🚫 Only the owner can view sudo users.")

    sudo_list = get_sudo_users()
    if not sudo_list:
        return await message.reply("No SUDO users found.")

    sudo_text = "\n".join([f"• `{uid}`" for uid in sudo_list])
    await message.reply(f"📝 SUDO Users:\n\n{sudo_text}")

# ✅ Force subscription toggle
@bot.on_message(filters.command("forceon"))
async def force_on(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        return await message.reply("🚫 Only the owner can enable force subscription.")

    set_force_check(True)
    await message.reply("✅ Force subscription enabled.")

@bot.on_message(filters.command("forceoff"))
async def force_off(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        return await message.reply("🚫 Only the owner can disable force subscription.")

    set_force_check(False)
    await message.reply("✅ Force subscription disabled.")

# ✅ Run bot
bot.run()
