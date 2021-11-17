import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.plugins.commands import all_commands
from main import bot

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.private, group=-1)
async def pre_message(_: Client, msg: Message) -> None:
    bot.audit(msg)
    bot.init_user(msg.from_user.id)

    if msg.text:
        if msg.text.startswith("/"):
            """指令交由後面處理"""
            if msg.text.split("/", maxsplit=2)[1] in all_commands:
                return

        if len(msg.text) == 4:
            await msg.reply(bot.get_question_topic(msg.text))
            return

        try_text: list[str] = msg.text.split("_", maxsplit=1)

        if len(try_text) == 2 and len(try_text[0]) == 4:
            await msg.reply(bot.answer_question(msg.from_user.id, try_text[0], try_text[1]))
            return

        await msg.reply(bot.random_reply())

        msg.stop_propagation()
