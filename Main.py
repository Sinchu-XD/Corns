from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

API_ID = 6067591
API_HASH = "94e17044c2393f43fda31d3afe77b26b"
BOT_TOKEN = "7758255754:AAH0wvr7nwSzEDq49UxhDi0hv0oVQvuRe_s"

REQUIRED_CHANNELS = ["@CornVideos4k", "@Itz_Your_4Bhi"]
db = {}  # Replace with persistent DB if needed

app = Client("ads-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Subscription checker
async def is_subscribed(client, user_id):
    try:
        for channel in REQUIRED_CHANNELS:
            chat = await client.get_chat(channel)
            member = await client.get_chat_member(chat.id, user_id)
            if member.status not in ("member", "administrator", "creator"):
                return False
        return True
    except Exception as e:
        print(f"Error in subscription check: {e}")
        return False

def get_token(user_id):
    if user_id in db and db[user_id]["expires"] > datetime.now():
        return db[user_id]
    return None

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id

    if not await is_subscribed(client, user_id):
        join_buttons = [
            [InlineKeyboardButton("🔗 Join Channel 1", url="https://t.me/CornVideos4k")],
            [InlineKeyboardButton("🔗 Join Channel 2", url="https://t.me/Itz_Your_4Bhi")],
        ]
        await message.reply(
            "**❌ You must join the channels to use this bot!**\n\n"
            "✅ Once done, press /start again.",
            reply_markup=InlineKeyboardMarkup(join_buttons)
        )
        return

    token_data = get_token(user_id)
    if not token_data:
        ad_buttons = [
            [InlineKeyboardButton("• Watch Ad •", url="https://t.me/CornVideos4k")],
            [InlineKeyboardButton("• How To Open •", url="https://t.me/Cornvideos4k/3")],
            [InlineKeyboardButton("• Buy Premium Plan •", url="https://t.me/LookRex")]
        ]
        await message.reply(
            "**📛 Your Ads Token Has Expired!**\n\n"
            "🔓 **Watch 3 pages to unlock for 1 day.**\n"
            "🎁 **Or Buy Premium to avoid ads!**",
            reply_markup=InlineKeyboardMarkup(ad_buttons)
        )
        return

    await message.reply("✅ Token Verified! You can now use the bot features.")

@app.on_message(filters.private & filters.command("get_token"))
async def get_token_command(client, message):
    user_id = message.from_user.id
    db[user_id] = {"expires": datetime.now() + timedelta(days=1)}
    await message.reply("🎉 Token activated for 1 day!")

app.run()
