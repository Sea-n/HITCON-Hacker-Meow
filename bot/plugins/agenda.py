import logging

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import CallbackQuery, InputMediaPhoto

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("agenda") & ~filters.forwarded)
async def agenda(cli: Client, msg: Message) -> None:
    keyboard = [[InlineKeyboardButton("格萊聽", "agenda_great"),
                 InlineKeyboardButton("天漾聽", "agenda_skyview"),
                 InlineKeyboardButton("康定聽", "agenda_kd"),
                 InlineKeyboardButton("天悅聽", "agenda_ty"),
                 InlineKeyboardButton("萬大聽", "agenda_wd")],
                [InlineKeyboardButton("Day 1 上午", "agenda_1A"),
                 InlineKeyboardButton("Day 1 下午", "agenda_1B"),
                 InlineKeyboardButton("Day 2 上午", "agenda_2A"),
                 InlineKeyboardButton("Day 2 下午", "agenda_2B")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await cli.send_photo(msg.chat.id, "https://i.imgur.com/jDeodyc.jpg",
                         "議程總覽\n你想看哪個演講廳", reply_markup=reply_markup)


@Client.on_callback_query(filters.regex('^agenda'))
async def map_callback(cli: Client, callback: CallbackQuery) -> None:
    media = None
    reply_markup = None
    if callback.data == "agenda":
        keyboard = [[InlineKeyboardButton("格萊聽", "agenda_great"),
                     InlineKeyboardButton("天漾聽", "agenda_skyview"),
                     InlineKeyboardButton("康定聽", "agenda_kd"),
                     InlineKeyboardButton("天悅聽", "agenda_ty"),
                     InlineKeyboardButton("萬大聽", "agenda_wd")],
                    [InlineKeyboardButton("Day 1", "agenda_Day1"),
                     InlineKeyboardButton("Day 2", "agenda_Day2")]]

        media = InputMediaPhoto("https://i.imgur.com/jDeodyc.jpg",
                                "議程總覽\n你想看哪個演講廳")

    elif callback.data == "agenda_great":
        keyboard = [[InlineKeyboardButton("金融業如何迎擊數位戰場", "agenda_great_1A"),
                     InlineKeyboardButton("Breaking Samsung's Root", "agenda_great_2A")],
                    [InlineKeyboardButton("主動式資安防禦策略", "agenda_great_1B"),
                     InlineKeyboardButton("From LNK to RCE", "agenda_great_2B")],
                    [InlineKeyboardButton("如何兼顧疫情控制與隱私保護", "agenda_great_1C"),
                     InlineKeyboardButton("RE: 從零開始的 OOO DEF", "agenda_great_2C")],
                    [InlineKeyboardButton("疫情後資安人才培育的挑戰", "agenda_great_1D"),
                     InlineKeyboardButton("Development of Signaling Spoofing", "agenda_great_2D")],
                    [InlineKeyboardButton("人工智慧能否為人類指引", "agenda_great_1E"),
                     InlineKeyboardButton("How I Hacked Facebook Again!", "agenda_great_2E")],
                    [InlineKeyboardButton("回議程總覽", "agenda")]]

        media = InputMediaPhoto("https://i.imgur.com/7JFS5PL.png",
                                "格萊聽議程總覽\n請選擇 XXX")

    else:
        log.debug(f"Unknown callback {callback.data}")
        await cli.answer_callback_query(callback.id, f"尚未實作 {callback.data}")
        return

    if media:
        reply_markup = InlineKeyboardMarkup(keyboard)
        await cli.edit_message_media(callback.message.chat.id,
                                     callback.message.message_id,
                                     media=media, reply_markup=reply_markup)

    await cli.answer_callback_query(callback.id)
