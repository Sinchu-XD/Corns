import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
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

@bot.on_message(filters.private & filters.command("start"))
@subscription_required
async def start(client, message: Message):
    user_id = message.from_user.id
    add_user(user_id)
    args = message.text.split()
    if len(args) > 1:
        file_id = args[1]
        file_data = get_file(file_id)
        if file_data:
            await message.reply_document(file_id, caption=f"📄 {file_data['file_name']}")
        else:
            await message.reply("❌ File not found.")
    else:
        await message.reply("Welcome! Send me a file to store.")

@bot.on_message(filters.private & (filters.document | filters.video | filters.photo))
@subscription_required
async def handle_file(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS and user_id not in SUDO_USERS:
        return await message.reply("🚫 You are not allowed to upload files.")

    media = message.document or message.video or message.photo
    file_id = media.file_id
    file_name = getattr(media, "file_name", "NoName")
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

@bot.on_message(filters.command("addch"))
@subscription_required
async def add_channel_command(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS and user_id not in SUDO_USERS:
        return await message.reply("🚫 You do not have permission to add channels.")

    try:
        slot, username = message.text.split()[1], message.text.split()[2]
        add_channel(slot, username)
        await message.reply(f"✅ Channel {username} added in slot {slot}.")
    except IndexError:
        await message.reply("⚠️ Usage: /addch <slot> <channel_username>")

@bot.on_message(filters.command("rmch"))
@subscription_required
async def remove_channel_command(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS and user_id not in SUDO_USERS:
        return await message.reply("🚫 You do not have permission to remove channels.")

    try:
        slot = message.text.split()[1]
        remove_channel(slot)
        await message.reply(f"✅ Channel in slot {slot} removed.")
    except IndexError:
        await message.reply("⚠️ Usage: /rmch <slot>")

@bot.on_message(filters.command("addsudo"))
@subscription_required
async def add_sudo(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        return await message.reply("🚫 Only the owner can add sudo users.")

    try:
        target_user = int(message.text.split()[1])
        add_sudo_user(target_user)
        await message.reply(f"✅ {target_user} added as SUDO.")
    except (IndexError, ValueError):
        await message.reply("⚠️ Usage: /addsudo <user_id>")

@bot.on_message(filters.command("rmsudo"))
@subscription_required
async def remove_sudo(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        return await message.reply("🚫 Only the owner can remove sudo users.")

    try:
        target_user = int(message.text.split()[1])
        remove_sudo_user(target_user)
        await message.reply(f"✅ {target_user} removed from SUDO.")
    except (IndexError, ValueError):
        await message.reply("⚠️ Usage: /rmsudo <user_id>")

@bot.on_message(filters.command("sudolist"))
@subscription_required
async def show_sudo_list(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        return await message.reply("🚫 Only the owner can view sudo users.")

    sudo_list = get_sudo_users()
    if not sudo_list:
        return await message.reply("No SUDO users found.")
    sudo_str = "\n".join([f"`{uid}`" for uid in sudo_list])
    await message.reply(f"📝 SUDO Users List:\n\n{sudo_str}")

@bot.on_message(filters.command("forceon"))
@subscription_required
async def force_on(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        return await message.reply("🚫 Only the owner can enable force subscription.")

    set_force_check(True)
    await message.reply("✅ Force subscription enabled.")

@bot.on_message(filters.command("forceoff"))
@subscription_required
async def force_off(client, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        return await message.reply("🚫 Only the owner can disable force subscription.")

    set_force_check(False)
    await message.reply("✅ Force subscription disabled.")

bot.run()
