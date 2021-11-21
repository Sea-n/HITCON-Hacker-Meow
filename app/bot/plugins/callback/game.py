import logging

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMedia, InputMediaPhoto

log: logging.Logger = logging.getLogger(__name__)
GAME_PHOTO: str = "https://i.imgur.com/Un9ZopT.png"


@Client.on_callback_query(filters.regex('^game'))
async def game_callback(cli: Client, callback: CallbackQuery) -> None:
    keyboard = [[
        InlineKeyboardButton("回到前面", "help"),
    ]]

    media: InputMedia = InputMediaPhoto(GAME_PHOTO, "Caption")

    await cli.edit_message_media(callback.message.chat.id,
                                 callback.message.message_id,
                                 media,
                                 reply_markup=InlineKeyboardMarkup(keyboard))

    await cli.answer_callback_query(callback.id)
