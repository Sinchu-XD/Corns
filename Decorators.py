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

from pyrogram import Client
from pyrogram.errors import UserNotParticipant
from Database import get_channels

async def check_user_joined(client: Client, user_id: int) -> bool:
    channels = await get_channels()
    for ch in channels:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status not in ("member", "administrator", "creator"):
                return False
        except UserNotParticipant:
            return False
        except Exception:
            continue
    return True
