import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.functions import get_whitelist

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.private, group=-1)
async def pre_check(_: Client, msg: Message) -> None:
    if msg.text.startswith("/start"):
        return

    if msg.from_user.id not in get_whitelist():
        await msg.reply("You have no rights!")
        msg.stop_propagation()
