import logging
import os

from pyrogram import Client, filters
from pyrogram.types import Message

from main import bot

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.group & ~ filters.edited)
async def irc_bridge(_: Client, msg: Message) -> None:
    if str(msg.chat.id) != os.getenv("TELEGRAM_GROUP"):
        return
    # TODO: ignore stickers, gifs, and others non-text messages
    irc_string: str = f"{msg.from_user.first_name}({msg.from_user.id}): {msg.text}"
    bot.irc.privmsg(os.getenv("IRC_CHANNEL"), irc_string)
