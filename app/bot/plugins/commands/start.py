import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from main import bot
from .help import help

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("start") & filters.private & ~ filters.forwarded)
async def start(cli: Client, msg: Message) -> None:
    if len(msg.command) == 2:
        token: str = msg.command[1]

        if len(token) == 4:
            await msg.reply(bot.get_question_topic(token))

        return

    await help(cli, msg)
