import logging

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

log: logging.Logger = logging.getLogger(__name__)

pic_url = "https://i.imgur.com/Un9ZopT.png"


@Client.on_message(filters.command("help") & filters.private & ~ filters.forwarded)
async def help(cli: Client, msg: Message) -> None:
    keyboard = [[
        InlineKeyboardButton("遊玩方式", "game"),
    ], [
        InlineKeyboardButton("HITCON 公告頻道", url="https://t.me/H17C0N"),
        InlineKeyboardButton("HITCON 聊天群組", url="https://t.me/HacksInTaiwan"),
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await cli.send_photo(msg.chat.id, pic_url,
                         "歡迎使用駭客喵喵\n\n點擊下方按鈕開始", reply_markup=reply_markup)
