import logging
from typing import Union

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from main import bot

log: logging.Logger = logging.getLogger(__name__)


@Client.on_callback_query(filters.all, group=-1)
async def pre_log_callback(cli: Client, callback: CallbackQuery) -> None:
    bot.audit(callback)
    session: Union[dict, None] = bot.get_session(callback.data)

    if session:
        s: str = f"<code>{session['zh']['title']}</code>\n" \
                 f"<code>{'=' * 10}</code>\n" \
                 f"Room: <code>{session['room']}</code>\n" \
                 f"Start time: {session['start']}\n" \
                 f"End time: {session['end']}\n" \
                 f"\n" \
                 f"Description: \n{session['zh']['description']}\n"

        keyboard: list[list[InlineKeyboardButton]] = [[]]

        if session['qa'] is not None:
            keyboard[-1].append(InlineKeyboardButton("QA", url=session['qa']))
            keyboard.append([])

        if session['slide'] is not None:
            keyboard[-1].append(InlineKeyboardButton("Slide", url=session['slide']))
            keyboard.append([])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await cli.edit_message_text(callback.message.chat.id,
                                    callback.message.message_id,
                                    s, reply_markup=reply_markup)

        await cli.answer_callback_query(callback.id)
        callback.stop_propagation()
