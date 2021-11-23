import logging

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMedia, InputMediaPhoto

log: logging.Logger = logging.getLogger(__name__)
GAME_PHOTO: str = "https://imgur.com/a/XhyDmzn"
INFO: str = """遊戲方式：
找尋會場中印有駭客貓歷險記的標示，打開 駭客喵喵 Telegram ，輸入題目標號 4 位數後，駭客喵喵將會要求你回答問題，回答成功將可以獲得相對應積分！

快去駭客貓貓放在會場中的 20 題題目標示吧！！據說最快完成全部題目的 20 名會眾將會獲得精美禮品哦！！"""


@Client.on_callback_query(filters.regex('^game'))
async def game_callback(cli: Client, callback: CallbackQuery) -> None:
    keyboard = [[
        InlineKeyboardButton("回到前面", "help"),
    ]]

    media: InputMedia = InputMediaPhoto(GAME_PHOTO, INFO)

    await cli.edit_message_media(callback.message.chat.id,
                                 callback.message.message_id,
                                 media,
                                 reply_markup=InlineKeyboardMarkup(keyboard))

    await cli.answer_callback_query(callback.id)
