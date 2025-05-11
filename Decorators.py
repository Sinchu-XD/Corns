# helpers/filters.py

from pyrogram import filters
from Config import Config

def owner_only(_, __, m):
    return m.from_user and m.from_user.id == Config.OWNER_ID

owner_only = filters.create(owner_only)

# Add below owner_only in helpers/filters.py

from Database import get_sudo_list

async def is_sudo(_, __, m):
    sudoers = await get_sudo_list()
    return m.from_user and m.from_user.id in sudoers

sudo_only = filters.create(is_sudo)

owner_or_sudo = owner_only | sudo_only

# helpers/check_join.py

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import UserNotParticipant, PeerIdInvalid
from pyrogram.enums import ChatMemberStatus
from functools import wraps
from Database import get_channels, get_force_check, get_sudo_list
from Config import Config

async def check_subscription(bot, user_id: int) -> bool:
    channels = await get_channels()
    for channel in channels:
        try:
            member = await bot.get_chat_member(username, user_id)
            if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return False
        except UserNotParticipant:
            return False
        except PeerIdInvalid:
            continue
        except Exception:
            continue
    return True

def subscription_required(func):
    @wraps(func)
    async def wrapper(client, update):
        user = update.from_user
        if not user:
            return

        user_id = user.id

        sudo_users = await get_sudo_list()
        if user_id == Config.OWNER_ID or user_id in sudo_users:
            return await func(client, update)

        if not await get_force_check():
            return await func(client, update)

        if not await check_subscription(client, user_id):
            channels = await get_channels()
            buttons = [
                [InlineKeyboardButton(f"🔗 Join Channel {slot}", url=f"https://t.me/{ch}")]
                for slot, ch in sorted(channels.items())
            ]
            buttons.append([InlineKeyboardButton("✅ I Joined", callback_data="check_join")])

            text = "🚫 **You must join all required channels to use this bot.**"
            markup = InlineKeyboardMarkup(buttons)

            if isinstance(update, Message):
                return await update.reply(text, reply_markup=markup)
            elif isinstance(update, CallbackQuery):
                return await update.message.edit(text, reply_markup=markup)

        return await func(client, update)

    return wrapper
