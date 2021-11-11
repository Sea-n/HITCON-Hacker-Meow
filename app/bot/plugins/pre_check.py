import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.magic_methods import get_whitelist
from main import bot

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.private, group=-1)
async def pre_check(_: Client, msg: Message) -> None:
    bot.audit(msg)

    if msg.text:
        if msg.text.startswith("/"):
            # 指令交由後面處理
            return

        if len(msg.text) == 4 and msg.text.isdigit():
            await msg.reply(bot.get_question(msg.text))
            return

        try_text: list[str] = msg.text.split("_", maxsplit=1)

        if len(try_text) == 2 and try_text[0].isdigit():
            await msg.reply(bot.answer_question(msg.from_user.id, try_text[0], try_text[1]))
            return

        await msg.reply(bot.random_reply())

        msg.stop_propagation()

    if msg.from_user.id not in get_whitelist():
        await msg.reply("駭客喵喵還不認識你喔，請跟我講通關密語或等到公開測試")
        msg.stop_propagation()
