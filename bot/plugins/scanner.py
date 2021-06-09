import logging
from uuid import uuid4

from typing import List
from pyrogram import Client, filters, raw
from pyrogram.raw.base import InputBotInlineResult
from pyrogram.types import CallbackGame, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InlineQuery, Message

log: logging.Logger = logging.getLogger(__name__)
GAME_SHORT_NAME: str = "QR_code"


@Client.on_inline_query()
async def inline_query(cli: Client, inline: InlineQuery) -> None:
    game_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Open game {GAME_SHORT_NAME}", callback_game=CallbackGame())],
        # game button **MUST** in (1, 1)
    ])

    inline_result: List[InputBotInlineResult] = [
        raw.types.InputBotInlineResultGame(
            id=str(uuid4()),
            short_name=GAME_SHORT_NAME,
            send_message=raw.types.InputBotInlineMessageGame(reply_markup=await game_keyboard.write(cli))
        )
    ]

    # equals to
    # await cli.answer_inline_query(inline.id, result, cache_time=0)
    await cli.send(
        raw.functions.messages.SetInlineBotResults(
            query_id=int(inline.id),
            results=inline_result,
            cache_time=0,
            gallery=None,
            private=None,
            next_offset=None,
            switch_pm=None
        )
    )


@Client.on_message(filters.command("game") & filters.private)
async def send_scanner(cli: Client, msg: Message):
    await cli.send_game(msg.chat.id, GAME_SHORT_NAME)


@Client.on_callback_query()
async def game_button(cli: Client, callback: CallbackQuery):
    if callback.game_short_name:
        await callback.answer(url="https://permission.site/")
        # await callback.answer(url="https://webqr.com/")
