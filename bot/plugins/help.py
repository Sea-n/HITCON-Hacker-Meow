import logging

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import CallbackQuery, InputMediaPhoto

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("help") & ~filters.forwarded)
@Client.on_message(filters.command("start") & ~filters.forwarded)
# TODO: split start to check token and add user to whitelist
async def help(cli: Client, msg: Message) -> None:
    keyboard = [[InlineKeyboardButton("議程資訊", "agenda"),
                 InlineKeyboardButton("精彩活動", "events")],
                [InlineKeyboardButton("交通方式", "traffinfo"),
                 InlineKeyboardButton("場地平面圖", "map")],
                [InlineKeyboardButton("HITCON 公告頻道", url="https://t.me/H17C0N"),
                 InlineKeyboardButton("HITCON 聊天群組", url="https://t.me/HacksInTaiwan")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await cli.send_photo(msg.chat.id, "https://i.imgur.com/Un9ZopT.png",
                         "歡迎使用駭客喵喵\n\n點擊下方按鈕開始", reply_markup=reply_markup)


@Client.on_callback_query(filters.regex('^help'))
async def help_callback(cli: Client, callback: CallbackQuery) -> None:
    if callback.data == "help":
        buttons = [{
            "議程資訊": "agenda",
            "精彩活動": "events"
        }, {
            "交通方式": "traffinfo",
            "場地平面圖": "map"
        }, {
            "HITCON 公告頻道": "https://t.me/H17C0N",
            "HITCON 聊天群組": "https://t.me/HacksInTaiwan"
        }]

        media = InputMediaPhoto("https://i.imgur.com/Un9ZopT.png",
                                "歡迎使用駭客喵喵\n\n點擊下方按鈕開始")

    else:
        log.debug(f"Unknown callback {callback.data}")
        await cli.answer_callback_query(callback.id, f"尚未實作 {callback.data}")
        return

    keyboard = []
    for k in buttons:
        row = []
        for txt in k:
            if 'https://' in k[txt]:
                button = InlineKeyboardButton(text=txt, url=k[txt])
            else:
                button = InlineKeyboardButton(text=txt, callback_data=k[txt])
            row.append(button)
        keyboard.append(row)

    await cli.edit_message_media(callback.message.chat.id,
                                 callback.message.message_id,
                                 media=media,
                                 reply_markup=InlineKeyboardMarkup(keyboard))

    await cli.answer_callback_query(callback.id)
