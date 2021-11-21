import logging

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMedia, InputMediaPhoto

log: logging.Logger = logging.getLogger(__name__)

PHOTO_URL = "https://i.imgur.com/Un9ZopT.png"


@Client.on_callback_query(filters.regex('^help'))
async def help_callback(cli: Client, callback: CallbackQuery) -> None:
    keyboard = [[
        InlineKeyboardButton("遊玩方式", "game"),
    ], [
        InlineKeyboardButton("HITCON 公告頻道", url="https://t.me/H17C0N"),
        InlineKeyboardButton("HITCON 聊天群組", url="https://t.me/HacksInTaiwan"),
    ]]

    media: InputMedia = InputMediaPhoto(PHOTO_URL,
                                        "歡迎使用駭客喵喵\n\n點擊下方按鈕開始")

    await cli.edit_message_media(callback.message.chat.id,
                                 callback.message.message_id,
                                 media,
                                 reply_markup=InlineKeyboardMarkup(keyboard))

    await cli.answer_callback_query(callback.id)
