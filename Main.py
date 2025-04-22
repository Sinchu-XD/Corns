from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from pyrogram.errors import UserNotParticipant

API_ID = 6067591
API_HASH = "94e17044c2393f43fda31d3afe77b26b"
BOT_TOKEN = "7758255754:AAH0wvr7nwSzEDq49UxhDi0hv0oVQvuRe_s"

REQUIRED_CHANNELS = ["@CornVideos4k", "@Itz_Your_4Bhi"]
db = {}

app = Client("ads-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Check if user is subscribed without needing admin access
async def is_subscribed(client, user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status in ("left",):
                return False
        except UserNotParticipant:
            return False
        except Exception as e:
            print(f"Check failed for {channel}: {e}")
            return False
    return True

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
            [InlineKeyboardButton("✅ I Joined", callback_data="check_sub")],
        ]
        await message.reply(
            "**❌ You must join both channels to use this bot!**\n\n"
            "👉 Then press **I Joined** to continue.",
            reply_markup=InlineKeyboardMarkup(join_buttons)
        )
        return

    token_data = get_token(user_id)
    if not token_data:
        ad_buttons = [
            [InlineKeyboardButton("• Watch Ad •", url="https://t.me/CornVideos4k")],
            [InlineKeyboardButton("• Buy Premium Plan •", url="https://t.me/LookRex")]
        ]
        await message.reply(
            "**📛 Ads Token Expired!**\n\n"
            "✅ View 3 pages to reactivate your token for 1 day.\n"
            "🚫 Avoid ads? Go premium!",
            reply_markup=InlineKeyboardMarkup(ad_buttons)
        )
        return

    await message.reply("✅ Token verified! You can now use the bot.")

@app.on_callback_query(filters.regex("check_sub"))
async def check_subscription(client, callback_query):
    user_id = callback_query.from_user.id
    if await is_subscribed(client, user_id):
        await callback_query.message.edit("✅ You’re now verified! Use the bot freely.")
    else:
        await callback_query.answer("❌ You still haven't joined the channels.", show_alert=True)

@app.on_message(filters.private & filters.command("get_token"))
async def get_token_command(client, message):
    user_id = message.from_user.id
    db[user_id] = {"expires": datetime.now() + timedelta(days=1)}
    await message.reply("🎉 Token activated for 1 day!")

app.run()
