from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import UserNotParticipant, PeerIdInvalid
from pyrogram.enums import ChatMemberStatus
from functools import wraps
from Database import get_all_channels, get_force_check, get_sudo_users
from Config import OWNER_IDS

async def check_subscription(bot, user_id: int) -> bool:
    channels = get_all_channels()
    for _, username in channels.items():
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

        # OWNER and SUDO_USERS bypass
        if user_id == OWNER_IDS or user_id in get_sudo_users():
            return await func(client, update)

        if not get_force_check():
            return await func(client, update)

        if not await check_subscription(client, user_id):
            channels = get_all_channels()
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
