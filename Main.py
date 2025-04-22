from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

API_ID = 6067591
API_HASH = "94e17044c2393f43fda31d3afe77b26b"
BOT_TOKEN = "7758255754:AAH0wvr7nwSzEDq49UxhDi0hv0oVQvuRe_s"

REQUIRED_CHANNELS = ["@CornVideos4k", "@Itz_Your_4Bhi"]

# Temporary in-memory DB (use a real database for production)
db = {}

app = Client("ads-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Check if user is subscribed to all required channels
async def is_subscribed(client, user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            print(f"Subscription check failed for {channel}: {e}")
            return False
    return True

# Get token if valid
def get_token(user_id):
    if user_id not in db or datetime.now() > db[user_id]["expires"]:
        return None
    return db[user_id]

# /start handler
@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id

    # Check subscription
    if not await is_subscribed(client, user_id):
        join_buttons = [
            [InlineKeyboardButton("Join Channel 1", url="https://t.me/CornVideos4k")],
            [InlineKeyboardButton("Join Channel 2", url="https://t.me/Itz_Your_4Bhi")],
        ]
        await message.reply(
            "**❌ Sorry! You must join the required channels to use this bot.**\n\n"
            "👉 Click the buttons below to join, then press /start again.",
            reply_markup=InlineKeyboardMarkup(join_buttons)
        )
        return

    # Check token status
    token_data = get_token(user_id)
    if not token_data:
        ad_buttons = [
            [InlineKeyboardButton("• Click Ad Link •", url="https://t.me/CornVideos4k")],
            [InlineKeyboardButton("• How to Complete It •", url="https://t.me/Cornvideos4k/3")],
            [InlineKeyboardButton("• Buy Premium •", url="https://t.me/LookRex")]
        ]
        await message.reply(
            "**🚫 Your Ads Token Has Expired!**\n\n"
            "**🕒 Token Timeout:** 1 Day\n\n"
            "**📌 What Is This?**\n"
            "You must pass 3 ad pages to unlock 1-day usage.\n\n"
            "**💎 Or Buy Premium To Skip Ads.**",
            reply_markup=InlineKeyboardMarkup(ad_buttons)
        )
        return

    # All good
    await message.reply("✅ Welcome back! Your token is active. You can now use the bot.")

# /get_token handler for activating 1-day token manually
@app.on_message(filters.private & filters.command("get_token"))
async def get_token_command(client, message):
    user_id = message.from_user.id
    db[user_id] = {"expires": datetime.now() + timedelta(days=1)}
    await message.reply("✅ Token activated for 1 day! You can now use the bot.")

app.run()
