import logging

from bot.functions import get_whitelist
from pyrogram import Client, filters
from pyrogram.types import Message

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.private, group=-1)
async def pre_check(_: Client, msg: Message) -> None:
    if msg.text and msg.text.startswith("/start"):
        return

    if msg.from_user.id not in get_whitelist():
        await msg.reply("駭客喵喵還不認識你喔，請跟我講通關密語或等到公開測試")
        msg.stop_propagation()
