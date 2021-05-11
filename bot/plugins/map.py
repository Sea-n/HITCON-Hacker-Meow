import logging

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import CallbackQuery, InputMediaPhoto

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("map") & ~filters.forwarded)
async def map(cli: Client, msg: Message) -> None:
    keyboard = [[InlineKeyboardButton("13 樓", "map_13F"),
                 InlineKeyboardButton("14 樓", "map_14F"),
                 InlineKeyboardButton("15 樓", "map_15F")],
                [InlineKeyboardButton("回主選單", "help")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await cli.send_photo(msg.chat.id, "https://i.imgur.com/uQLAd4x.png",
                         "場地總覽\n你想看哪層樓", reply_markup=reply_markup)


@Client.on_callback_query(filters.regex('^map'))
async def map_callback(cli: Client, callback: CallbackQuery) -> None:
    media = None
    reply_markup = None
    if callback.data == "map":
        keyboard = [[InlineKeyboardButton("13 樓", "map_13F"),
                     InlineKeyboardButton("14 樓", "map_14F"),
                     InlineKeyboardButton("15 樓", "map_15F")],
                    [InlineKeyboardButton("回主選單", "help")]]

        media = InputMediaPhoto("https://i.imgur.com/uQLAd4x.png",
                                "場地總覽\n你想看哪層樓")

    elif callback.data == "map_13F":
        keyboard = [[InlineKeyboardButton("議程（格萊聽）", "agenda_great"),
                     InlineKeyboardButton("XX 活動（天漾聽）", "events_skyview")],
                    [InlineKeyboardButton("回樓層圖", "map")]]

        media = InputMediaPhoto("https://i.imgur.com/MqYzHd5.png",
                                "這是 13 樓的平面圖\n對 XX 議程、XX 活動有興趣嗎")

    elif callback.data == "map_14F":
        keyboard = [[InlineKeyboardButton("攤位（康定聽）", "booth_kd"),
                     InlineKeyboardButton("贊助商（艋舺聽）", "booth_bk"),
                     InlineKeyboardButton("XX 活動（萬大聽）", "events_wd")],
                    [InlineKeyboardButton("回樓層圖", "map")]]

        media = InputMediaPhoto("https://i.imgur.com/y7UcbyJ.png",
                                "這是 14 樓的平面圖\n對 XX 攤位、XX 活動有興趣嗎")

    elif callback.data == "map_15F":
        keyboard = [[InlineKeyboardButton("議程（天悅聽）", "agenda_ty"),
                     InlineKeyboardButton("議程（天嵐聽）", "agenda_tl"),
                     InlineKeyboardButton("攤位（天闊聽）", "booth_tk")],
                    [InlineKeyboardButton("回樓層圖", "map")]]

        media = InputMediaPhoto("https://i.imgur.com/F0YKoOX.png",
                                "這是 15 樓的平面圖\n對 XX 議程、XX 攤位有興趣嗎")

    else:
        log.debug(f"Unknown callback {callback.data}")
        await cli.answer_callback_query(callback.id, f"尚未實作 {callback.data}")
        return

    reply_markup = InlineKeyboardMarkup(keyboard)
    await cli.edit_message_media(callback.message.chat.id,
                                 callback.message.message_id,
                                 media=media, reply_markup=reply_markup)

    await cli.answer_callback_query(callback.id)
