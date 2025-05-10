import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
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

# 🚨 Helpers
def is_admin(uid):
    return uid in OWNER_IDS or uid in SUDO_USERS

# 🟢 START COMMAND
@bot.on_message(filters.command("start") & filters.private)
@subscription_required
async def start_command(client, message: Message):
    user_id = message.from_user.id
    channels = get_all_channels()

    if is_admin(user_id):
        if len(channels) < 2:
            return await message.reply("⚠️ Add at least **2 channels** using:\n`/addch <slot> <@channel>`")
        return await message.reply(
            "👋 Welcome Admin!\n\n📤 Send any file to convert into a sharable link.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📡 View Channels", callback_data="view_channels")]])
        )

    if channels:
        channel_url = f"https://t.me/{list(channels.values())[0]}"
        await message.reply(
            "📥 Get files and content from our channels.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔗 Open Channel", url=channel_url)]])
        )
    else:
        await message.reply("❌ No content available. Try again later.")

# 📤 FILE HANDLER
@bot.on_message(filters.private & (filters.document | filters.video | filters.photo | filters.animation))
@subscription_required
async def handle_file(client, message: Message):
    user_id = message.from_user.id
    mention = message.from_user.mention

    if not is_admin(user_id):
        return await message.reply("🚫 You are not allowed to upload files.")

    if len(get_all_channels()) < 2:
        return await message.reply("⚠️ Please add at least **2 channels** using `/addch` first.")

    media = message.document or message.video or message.photo or message.animation
    file_id = media.file_id

    if hasattr(media, "file_name"):
        file_name = media.file_name
    elif message.photo:
        file_name = f"Photo_{message.id}.jpg"
    elif message.video:
        file_name = f"Video_{message.id}.mp4"
    elif message.animation:
        file_name = f"GIF_{message.id}.mp4"
    else:
        file_name = f"File_{message.id}"

    add_file(file_id, file_name, user_id)
    bot_username = (await client.get_me()).username
    deep_link = f"https://t.me/{bot_username}?start={file_id}"

    await message.reply(
        f"✅ **Saved** as `{file_name}`\n🔗 [Open File Link]({deep_link})",
        disable_web_page_preview=True
    )

    await client.send_message(
        LOG_GROUP_ID,
        f"📥 `{file_name}` uploaded by {mention}\n🔗 [File Link]({deep_link})",
        disable_web_page_preview=True
    )

# 📋 CHANNEL MANAGEMENT
@bot.on_message(filters.command("addch"))
async def add_channel_command(client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply("🚫 You can't add channels.")

    try:
        _, slot, username = message.text.split(maxsplit=2)
        channels = get_all_channels()
        if slot in channels:
            return await message.reply(f"⚠️ Slot `{slot}` is in use by @{channels[slot]}. Use `/rmch {slot}` first.")
        add_channel(slot, username)
        await message.reply(f"✅ Added @{username} to slot `{slot}`.")
    except ValueError:
        await message.reply("⚠️ Usage: `/addch <slot> <channel_username>`")

@bot.on_message(filters.command("rmch"))
async def remove_channel_command(client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply("🚫 You can't remove channels.")

    try:
        _, slot = message.text.split(maxsplit=1)
        remove_channel(slot)
        await message.reply(f"✅ Removed channel from slot `{slot}`.")
    except ValueError:
        await message.reply("⚠️ Usage: `/rmch <slot>`")

@bot.on_message(filters.command("channels"))
async def list_channels(client, message: Message):
    if not is_admin(message.from_user.id):
        return await message.reply("🚫 You can't view channels.")

    channels = get_all_channels()
    if not channels:
        return await message.reply("📭 No channels added.")
    
    text = "\n".join([f"🔢 Slot `{k}` → @{v}" for k, v in channels.items()])
    await message.reply(f"📡 **Connected Channels:**\n\n{text}")

# 🧑‍💻 SUDO MANAGEMENT
@bot.on_message(filters.command("addsudo"))
async def add_sudo(client, message: Message):
    if message.from_user.id not in OWNER_IDS:
        return await message.reply("🚫 Only owner can add sudo users.")
    try:
        _, user_id = message.text.split(maxsplit=1)
        add_sudo_user(int(user_id))
        await message.reply(f"✅ `{user_id}` added as sudo.")
    except Exception:
        await message.reply("⚠️ Usage: `/addsudo <user_id>`")

@bot.on_message(filters.command("rmsudo"))
async def remove_sudo(client, message: Message):
    if message.from_user.id not in OWNER_IDS:
        return await message.reply("🚫 Only owner can remove sudo users.")
    try:
        _, user_id = message.text.split(maxsplit=1)
        remove_sudo_user(int(user_id))
        await message.reply(f"✅ `{user_id}` removed from sudo.")
    except Exception:
        await message.reply("⚠️ Usage: `/rmsudo <user_id>`")

@bot.on_message(filters.command("sudolist"))
async def show_sudo_list(client, message: Message):
    if message.from_user.id not in OWNER_IDS:
        return await message.reply("🚫 Only owner can view sudo users.")
    sudo = get_sudo_users()
    if not sudo:
        return await message.reply("❌ No sudo users.")
    await message.reply("👤 **SUDO Users:**\n\n" + "\n".join([f"• `{i}`" for i in sudo]))

# 🔒 FORCE SUBSCRIPTION
@bot.on_message(filters.command("forceon"))
async def force_on(client, message: Message):
    if message.from_user.id not in OWNER_IDS:
        return await message.reply("🚫 Only owner can enable force.")
    set_force_check(True)
    await message.reply("✅ Force subscription enabled.")

@bot.on_message(filters.command("forceoff"))
async def force_off(client, message: Message):
    if message.from_user.id not in OWNER_IDS:
        return await message.reply("🚫 Only owner can disable force.")
    set_force_check(False)
    await message.reply("✅ Force subscription disabled.")

# 🆘 HELP
@bot.on_message(filters.command("help"))
async def help_command(client, message: Message):
    help_text = """
📚 **Bot Commands:**

👤 **User:**
• `/start` - Start bot & view content

🛠 **Admin:**
• `/addch <slot> <@channel>` - Add a channel
• `/rmch <slot>` - Remove channel
• `/channels` - List channels

🔐 **Sudo Control:**
• `/addsudo <user_id>` - Add sudo
• `/rmsudo <user_id>` - Remove sudo
• `/sudolist` - List sudo users

📌 **Other:**
• `/forceon` - Enable force subscription
• `/forceoff` - Disable force subscription
"""
    await message.reply(help_text)

# ✅ RUN BOT
bot.run()
