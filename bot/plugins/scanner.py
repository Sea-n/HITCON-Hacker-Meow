import logging
from uuid import uuid4

from pyrogram import Client, filters, raw
from pyrogram.types import InlineQuery, Message

log: logging.Logger = logging.getLogger(__name__)
GAME_SHORT_NAME: str = "QR_code"


@Client.on_inline_query()
async def inline_query(cli: Client, inline: InlineQuery) -> None:
    # equals to
    # await cli.answer_inline_query(inline.id, result, cache_time=0)
    await cli.send(
        raw.functions.messages.SetInlineBotResults(
            query_id=int(inline.id),
            results=[raw.types.InputBotInlineResultGame(
                id=str(uuid4()),
                short_name=GAME_SHORT_NAME,
                send_message=raw.types.InputBotInlineMessageGame(reply_markup=None)
            )],
            cache_time=0,
            gallery=None,
            private=None,
            next_offset=None,
            switch_pm=None
        )
    )


@Client.on_message(filters.command("send_scanner") & filters.private)
async def send_scanner(cli: Client, msg: Message):
    await cli.send_game(msg.chat.id, GAME_SHORT_NAME)
