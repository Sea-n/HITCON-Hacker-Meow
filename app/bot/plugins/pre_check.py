import logging

from pyrogram import Client, filters
from pyrogram.types import Message
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

        results: Results = bot.search(msg.text)

        if len(results) > 0:
            s: str = f"駭客喵喵找到了 {len(results)} 個你可能在找的議程\n"

            for index, r in enumerate(results):
                # TODO: 改寫成按鈕形式，點擊後可帶出議程基本資訊
                s += f"第 {index + 1} 個標題為：\n<code>{r['title']}</code>\n"

            await msg.reply(s)

        else:
            await msg.reply(bot.random_reply())

        msg.stop_propagation()

    if msg.from_user.id not in get_whitelist():
        await msg.reply("駭客喵喵還不認識你喔，請跟我講通關密語或等到公開測試")
        msg.stop_propagation()
