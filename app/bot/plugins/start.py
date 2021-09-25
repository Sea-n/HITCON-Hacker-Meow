import logging
import os

import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from bot.functions import add_whitelist, get_whitelist
from models import User, db
from .help import help

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("start"))
async def start(cli: Client, msg: Message) -> None:
    if len(msg.command) == 2:
        token: str = msg.command[1]

        if token == os.getenv("VERIFY"):
            add_whitelist(msg.from_user.id)
            await msg.reply("歡迎使用！")
        elif len(token) == 41:
            api_url: str = os.getenv("BASE_URL") + "api/v1/tg/token"
            data = {"code": token}
            response = requests.post(api_url, data=data)

            if response.json().get("success"):
                user: User = User()
                user.uid = msg.from_user.id
                user.jwt_token = response.json().get("token")

                with db.session() as session:
                    session.add(user)
                    session.commit()

                await msg.reply("成功完成綁定")
            else:
                await msg.reply("你是...?")
        else:
            await msg.reply("通關密語錯誤！")

        return

    if msg.from_user.id not in get_whitelist():
        await msg.reply("駭客喵喵還不認識你喔，請跟我講通關密語或等到公開測試")
        return

    await help(cli, msg)
