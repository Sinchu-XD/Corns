from Config import Config
from telethon.tl.types import Update
from telethon import events
from Database import get_sudo_list
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError, ChatAdminRequiredError
from telethon.tl.types import ChatParticipantBanned
from Database import get_channels, get_force_check, get_sudo_list, get_main_channel
from Config import Config
from telethon import events, Button
from functools import wraps

async def check_subscription(client, user_id: int) -> bool:
    channels = await get_channels()
    if not channels:
        return True

    usernames = list(channels.values()) if isinstance(channels, dict) else channels

    for channel in usernames:
        try:
            result = await client(GetParticipantRequest(channel, user_id))
            if isinstance(result.participant, ChatParticipantBanned):
                return False
        except UserNotParticipantError:
            return False
        except ChatAdminRequiredError:
            continue  # Skip if bot can't access details
        except Exception as e:
            print(f"[Subscription Check Error] {e}")
            continue
    return True

def subscription_required(func):
    @wraps(func)
    async def wrapper(event: events.NewMessage.Event):
        user_id = event.sender_id
        if await check_subscription(event.client, user_id):
            return await func(event)

        channels = await get_channels()
        main_channel = await get_main_channel()
        buttons = []

        usernames = list(channels.values()) if isinstance(channels, dict) else channels
        for username in usernames:
            buttons.append([Button.url(f"📡 Join @{username}", f"https://t.me/{username}")])
        
        buttons.append([Button.inline("✅ I Joined", b"check_join")])
        if main_channel:
            buttons.append([Button.url("🏠 Main Channel", f"https://t.me/{main_channel}")])

        await event.respond(
            "📥 Please join all required channels to use this bot:",
            buttons=buttons
        )
    return wrapper
    
def owner_only(event: events.NewMessage.Event):
    return event.sender_id == Config.OWNER_ID

async def is_sudo(event: events.NewMessage.Event):
    sudoers = await get_sudo_list()
    return event.sender_id in sudoers

async def owner_or_sudo(event: events.NewMessage.Event):
    if event.sender_id == Config.OWNER_ID:
        return True
    sudoers = await get_sudo_list()
    return event.sender_id in sudoers

