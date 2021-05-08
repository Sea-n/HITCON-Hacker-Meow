import logging

from pyrogram import Client, filters
from pyrogram.types import Message

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.all)
async def test(cli: Client, msg: Message) -> None:
    log.debug(cli)
    log.debug(msg)
