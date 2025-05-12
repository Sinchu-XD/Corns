from pyrogram import Client, filters
from pyrogram.types import Message
from Bot import bot
from Database import add_channel, remove_channel, get_channels
from Decorators import owner_or_sudo
import re

# Helper to clean and extract valid identifiers
def extract_channel_input(raw: str) -> str:
    # Remove URL prefix if present
    if raw.startswith("https://t.me/"):
        raw = raw.replace("https://t.me/", "")
    elif raw.startswith("t.me/"):
        raw = raw.replace("t.me/", "")

    # Remove leading @ if present
    if raw.startswith("@"):
        raw = raw[1:]

    return raw

@bot.on_message(filters.command("addchannel") & owner_or_sudo)
async def add_channel_cmd(c: Client, m: Message):
    if len(m.command) < 2:
        return await m.reply("Usage:\n`/addchannel @username | -100id | t.me/link`")
    raw_input = m.command[1]
    channel_ref = extract_channel_input(raw_input)

    # Basic validation
    if not (channel_ref.startswith("joinchat/") or channel_ref.startswith("c/") or channel_ref.startswith("-100") or re.match(r"^[A-Za-z0-9_]+$", channel_ref)):
        return await m.reply("❌ Invalid channel format.")

    await add_channel(channel_ref)
    await m.reply(f"✅ Added `{channel_ref}` to required join list.")

@bot.on_message(filters.command("rmchannel") & owner_or_sudo)
async def remove_channel_cmd(c: Client, m: Message):
    if len(m.command) < 2:
        return await m.reply("Usage:\n`/rmchannel @username | -100id | t.me/link`")
    raw_input = m.command[1]
    channel_ref = extract_channel_input(raw_input)
    await remove_channel(channel_ref)
    await m.reply(f"❌ Removed `{channel_ref}` from required join list.")

@bot.on_message(filters.command("channelslist") & owner_or_sudo)
async def list_channels_cmd(c: Client, m: Message):
    channels = await get_channels()
    if not channels:
        return await m.reply("🚫 No required channels set.")
    msg = "**📢 Required Channels:**\n" + "\n".join([f"- `{ch}`" for ch in channels])
    await m.reply(msg)
