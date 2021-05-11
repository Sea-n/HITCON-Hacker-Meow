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
    if callback.data == "agenda":
        buttons = [{
            "格萊聽": "agenda_great",
            "天漾聽": "agenda_skyview",
            "康定聽": "agenda_kd",
            "天悅聽": "agenda_ty",
            "萬大聽": "agenda_wd"
        }, {
            "Day 1": "agenda_Day1",
            "Day 2": "agenda_Day2"
        }]

        media = InputMediaPhoto("https://i.imgur.com/jDeodyc.jpg",
                                "議程總覽\n你想看哪個演講廳")

    elif callback.data == "agenda_great":
        buttons = [{
            "金融業如何迎擊數位戰場": "agenda_great_1A",
            "Breaking Samsung's Root": "agenda_great_2A"
        }, {
            "主動式資安防禦策略": "agenda_great_1B",
            "From LNK to RCE": "agenda_great_2B"
        }, {
            "如何兼顧疫情控制與隱私保護": "agenda_great_1C",
            "RE: 從零開始的 OOO DEF": "agenda_great_2C"
        }, {
            "疫情後資安人才培育的挑戰": "agenda_great_1D",
            "Development of Signaling Spoofing": "agenda_great_2D"
        }, {
            "人工智慧能否為人類指引": "agenda_great_1E",
            "How I Hacked Facebook Again!": "agenda_great_2E"
        }, {
            "回議程總覽": "agenda"
        }]

        media = InputMediaPhoto("https://i.imgur.com/7JFS5PL.png",
                                "格萊聽議程總覽\n請選擇 XXX")

    elif callback.data == "agenda_Day1":
        buttons = [{
            "11:00 - 11:50": "agenda_Day1A",
            "13:00 - 13:50": "agenda_Day1B",
        }, {
            "14:00 - 14:50": "agenda_Day1C",
            "15:30 - 16:20": "agenda_Day1D",
            "16:30 - 17:20": "agenda_Day1E"
        }, {
            "回議程總覽": "agenda"
        }]

        media = InputMediaPhoto("https://i.imgur.com/SsAfqPg.png",
                                "Day 1 議程總覽\n請選擇時段")

    elif callback.data == "agenda_Day2":
        buttons = [{
            "09:20 - 10:10": "agenda_Day2A",
            "10:20 - 11:10": "agenda_Day2B",
            "11:20 - 12:10": "agenda_Day2C",
        }, {
            "13:50 - 14:40": "agenda_Day2D",
            "14:50 - 15:40": "agenda_Day2E",
        }, {
            "回議程總覽": "agenda"
        }]

        media = InputMediaPhoto("https://i.imgur.com/T2WWUla.png",
                                "Day 2 議程總覽\n請選擇時段")

    elif callback.data == "agenda_Day1A":
        buttons = [{
            "金融業如何迎擊數位戰場的第一道烽火": "agenda_Day1A1",
            "通訊網路安全研究，從 GSM 到 5G NR": "agenda_Day1B2",
        }, {
            "練蠱大賽": "agenda_Day1C3",
            "A Million Boluses: Discovery and Disclosure": "agenda_Day1D4",
            "IoT Hacking 101": "agenda_Day1E5"
        }, {
            "回 Day 1 議程": "agenda_Day1"
        }]

        media = InputMediaPhoto("https://i.imgur.com/IicQq8u.png",
                                "Day 1 上午 11:00 - 11:50 議程\n請選擇場次")

    elif callback.data in ["agenda_great_1A", "agenda_Day1A1"]:
        buttons = [{
            "Slido": "https://app.sli.do/event/ycm3yt5t",
            "議程共筆": "https://hackmd.io/FHbMehMSTsSq0aulU7GlKQ",
            "會場地圖": "map_13F",
        }, {
            "回到格萊聽": "agenda_great",
            "同時段議程": "agenda_Day1A",
        }]

        media = InputMediaPhoto("https://i.imgur.com/WmTrCaK.png",
                                "<b>[ HITCON 論壇 ] 金融業如何迎擊數位戰場的第一道烽火</b>\n\n 金融業是全國資安首當其衝的攻擊熱點，各單位的資安策略及措施，也非常適合各產業企業做為參考，有做為標竿的作用。本次探討的方向會針對「防禦機制的有效性評估」、「供應鏈安全」、「資安策略及預算投放」進行，以期透過這樣的討論讓聽眾知道金融機構資安的超前部署，增加民眾對資安的信心，也做為其他業者的表率。")

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
