import logging

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from whoosh.searching import Results

from bot.functions import get_whitelist
from main import bot

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.private, group=-1)
async def pre_check(_: Client, msg: Message) -> None:
    bot.audit(msg)

    if msg.text:
        if msg.text.startswith("/"):
            # 指令交由後面處理
            return

        results: Results = bot.search_keyword(msg.text)

        if len(results) > 0:
            s: str = f"駭客喵喵找到了 {len(results)} 個你可能在找的議程\n"

            keyboard: list[list[InlineKeyboardButton]] = [[]]

            for index, r in enumerate(results):
                keyboard[index].append(
                    InlineKeyboardButton(
                        r["title"], r["id"]
                    )
                )
                keyboard.append([])

            reply_markup = InlineKeyboardMarkup(keyboard)
            await msg.reply(s, reply_markup=reply_markup)

        else:
            await msg.reply(bot.random_reply())

        msg.stop_propagation()

    if msg.from_user.id not in get_whitelist():
        await msg.reply("駭客喵喵還不認識你喔，請跟我講通關密語或等到公開測試")
        msg.stop_propagation()
