from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import json, os

API_ID = 6067591
API_HASH = "94e17044c2393f43fda31d3afe77b26b"
BOT_TOKEN = "7758255754:AAH0wvr7nwSzEDq49UxhDi0hv0oVQvuRe_s"
REQUIRED_CHANNELS = ["@CornVideos4k", "@Itz_Your_4Bhi"]

db = {}  # This will be your in-memory user database. Replace with DB for production.

app = Client("ads-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_subscribed(user_id):
    # Dummy subscription check (implement real one with `get_chat_member`)
    return all(True for _ in REQUIRED_CHANNELS)

def get_token(user_id):
    if user_id not in db or datetime.now() > db[user_id]["expires"]:
        return None
    return db[user_id]

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id

    if not is_subscribed(user_id):
        join_buttons = [
            [InlineKeyboardButton("Join Channel", url="https://t.me/Cornvideos4k"),
             InlineKeyboardButton("Developer Bc", url="https://t.me/Itz_Your_4Bhi")],
        ]
        await message.reply(
            "**Sorry Dude You Need To Join These Channels**\n\n**So Please Click Below To Join Channel 🔥**",
            reply_markup=InlineKeyboardMarkup(join_buttons)
        )
        return

    token_data = get_token(user_id)
    if not token_data:
        # No valid token
        ad_buttons = [
            [InlineKeyboardButton("•Click Here•", url="https://t.me/Cornvideos4k")],
            [InlineKeyboardButton("•How To Open This Link•", url="https://t.me/Cornvideos4k/3")],
            [InlineKeyboardButton("•Buy Premium Plan•", url="https://t.me/LookRex")]
        ]
        await message.reply(
            "**Your Ads Token Is Expired, Refresh Your Token And Try Again.**\n\n"
            "**Token Timeout:** 1 days\n\n"
            "**What Is The Token?**\n\n"
            "This Is An Ads Token. If You Pass 3 Page Ad, You Can Use The Bot For 1 day After Passing The Ad.\n\n"
            "**Take Premium Plan And Avoid Adds ❣️❣️.**",
            reply_markup=InlineKeyboardMarkup(ad_buttons)
        )
        return

    await message.reply("✅ Welcome! You are verified and your token is active.")

@app.on_message(filters.command("get_token"))
async def get_token_command(client, message):
    user_id = message.from_user.id
    db[user_id] = {"expires": datetime.now() + timedelta(days=1)}
    await message.reply("✅ Token Activated For 1 Day!")

app.run()
