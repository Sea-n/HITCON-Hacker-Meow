import logging

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

log: logging.Logger = logging.getLogger(__name__)


@Client.on_callback_query(filters.regex('^help'))
async def help_callback(cli: Client, callback: CallbackQuery) -> None:
    if callback.data == "help":
        keyboard = [[
            InlineKeyboardButton("精彩活動", "events"),
        ], [
            InlineKeyboardButton("HITCON 公告頻道", url="https://t.me/H17C0N"),
            InlineKeyboardButton("HITCON 聊天群組", url="https://t.me/HacksInTaiwan"),
        ]]

        media = InputMediaPhoto("https://i.imgur.com/Un9ZopT.png",
                                "歡迎使用駭客喵喵\n\n點擊下方按鈕開始")

    else:
        log.debug(f"Unknown callback {callback.data}")
        await cli.answer_callback_query(callback.id, f"尚未實作 {callback.data}")
        return

    await cli.edit_message_media(callback.message.chat.id,
                                 callback.message.message_id,
                                 media=media,
                                 reply_markup=InlineKeyboardMarkup(keyboard))

    await cli.answer_callback_query(callback.id)
