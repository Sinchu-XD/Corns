# plugins/channel.py

from pyrogram import Client, filters
from pyrogram.types import Message
from Bot import bot
from Database import add_channel, remove_channel, get_channels
from Decorators import owner_or_sudo

@bot.on_message(filters.command("addchannel") & owner_or_sudo))
async def add_channel_cmd(c: Client, m: Message):
    if len(m.command) < 2:
        return await m.reply("Usage: `/addchannel @channelusername`")
    ch = m.command[1]
    if ch.startswith("@"):
        ch = ch[1:]
    await add_channel(ch)
    await m.reply(f"✅ Added {ch} to required join list.")

@bot.on_message(filters.command("rmchannel") & owner_or_sudo)
async def remove_channel_cmd(c: Client, m: Message):
    if len(m.command) < 2:
        return await m.reply("Usage: `/rmchannel @channelusername`")
    ch = m.command[1]
    await remove_channel(ch)
    await m.reply(f"❌ Removed {ch} from required join list.")

@bot.on_message(filters.command("channelslist") & owner_or_sudo)
async def list_channels_cmd(c: Client, m: Message):
    channels = await get_channels()
    if not channels:
        return await m.reply("No required channels set.")
    msg = "**📢 Required Channels:**\n" + "\n".join([f"- {ch}" for ch in channels])
    await m.reply(msg)
  
