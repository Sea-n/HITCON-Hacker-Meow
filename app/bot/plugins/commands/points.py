import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from main import bot

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("points") & filters.private & ~ filters.forwarded)
async def events(_: Client, msg: Message) -> None:
    points: int = bot.get_user_points(msg.from_user.id)

    await msg.reply(f"您目前有 <code>{points}</code> 分")
