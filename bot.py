
import os
import asyncio
import logging

from pyrogram import Client, filters, idle

# ================= CONFIG =================

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

GAME_BOT_USERNAME = "cricketrivalrybot"

SIX_VIDEO = "videos/six.mp4"
FOUR_VIDEO = "videos/four.mp4"
OUT_VIDEO = "videos/out.mp4"

# ===========================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User account: listens to game messages
listener = Client(
    "cheer_listener",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Bot account: sends videos
cheer_bot = Client(
    "cheer_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Video captions
CAPTIONS = {
    "six": "🔥 WHAT A SIX! 💥\n🏏 Stadium motham shake avvali!",
    "four": "💥 BEAUTIFUL FOUR! 🔥\n🏏 Super shot!",
    "out": "💀 WICKET DOWN!\n🔥 Game lo twist start ayyindhi!"
}


async def send_celebration(message, event):
    videos = {
        "six": SIX_VIDEO,
        "four": FOUR_VIDEO,
        "out": OUT_VIDEO
    }

    video = videos[event]

    if not os.path.isfile(video):
        logger.error("Video not found: %s", video)
        return

    try:
        await cheer_bot.send_video(
            chat_id=message.chat.id,
            video=video,
            caption=CAPTIONS[event],
            reply_to_message_id=message.id
        )

        logger.info("%s video sent", event.upper())

    except Exception as e:
        logger.exception("Video sending failed: %s", e)


@listener.on_message(filters.group & filters.text)
async def detect_game_result(client, message):

    # Only Cricket Rivalry bot messages
    sender = message.from_user

    if not sender or not sender.username:
        return

    if sender.username.lower() != GAME_BOT_USERNAME:
        return

    text = message.text.upper().strip()

    # Detect results
    if "WICKET!" in text or "💥 WICKET" in text:
        await send_celebration(message, "out")

    elif "SIX!" in text or "🔥 SIX" in text:
        await send_celebration(message, "six")

    elif "FOUR!" in text or "🏏 FOUR" in text:
        await send_celebration(message, "four")


async def main():

    if not API_ID or not API_HASH or not SESSION_STRING or not BOT_TOKEN:
        raise ValueError("Please configure API_ID, API_HASH, SESSION_STRING and BOT_TOKEN")

    print("🔥 Starting Telugu Friends Cheer Bot...")

    await listener.start()
    await cheer_bot.start()

    print("✅ Pyrogram listener started!")
    print("✅ Cheer Bot started!")
    print("🏏 Waiting for SIX, FOUR and WICKET...")

    try:
        await idle()
    finally:
        await cheer_bot.stop()
        await listener.stop()


if __name__ == "__main__":
    asyncio.run(main())
  
