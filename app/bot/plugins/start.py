import logging
import os

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.magic_methods import add_whitelist, get_whitelist
from main import bot
from .help import help

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("start"))
async def start(cli: Client, msg: Message) -> None:
    if len(msg.command) == 2:
        token: str = msg.command[1]

        if token == os.getenv("VERIFY"):
            add_whitelist(msg.from_user.id)
            await msg.reply("歡迎使用！")

        elif token.isdigit():  # TODO: 0 開頭字串檢查
            await msg.reply(bot.get_question_topic(token))

        else:
            await msg.reply("通關密語錯誤！")

        return

    if msg.from_user.id not in get_whitelist():
        await msg.reply("駭客喵喵還不認識你喔，請跟我講通關密語或等到公開測試")
        return

    await help(cli, msg)
