import logging

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import CallbackQuery, InputMediaPhoto

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("traffinfo") & ~filters.forwarded)
async def traffinfo(cli: Client, msg: Message) -> None:
    keyboard = [[InlineKeyboardButton("捷運 龍山寺站", "traffinfo_mrt"),
                 InlineKeyboardButton("台鐵 萬華站", "traffinfo_tra"),
                 InlineKeyboardButton("公車", "traffinfo_bus")],
                [InlineKeyboardButton("自行開車", "traffinfo_car"),
                 InlineKeyboardButton("Google 地圖", "https://goo.gl/maps/5YWkR4cMPNS3jekF9")],
                [InlineKeyboardButton("回主選單", "help")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await cli.send_photo(msg.chat.id, "https://i.imgur.com/t19xHxU.png",
                         "格萊天漾大飯店\n\nWanhua Dist., Bangka Blvd, No. 101", reply_markup=reply_markup)


@Client.on_callback_query(filters.regex('^traffinfo'))
async def traffinfo_callback(cli: Client, callback: CallbackQuery) -> None:
    if callback.data == "traffinfo":
        buttons = [{
            "捷運 龍山寺站": "traffinfo_mrt",
            "台鐵 萬華站": "traffinfo_tra",
            "公車": "traffinfo_bus"
        }, {
            "自行開車": "traffinfo_car",
            "Google 地圖": "https://goo.gl/maps/5YWkR4cMPNS3jekF9"
        }, {
            "回主選單": "help"
        }]

        media = InputMediaPhoto("https://i.imgur.com/t19xHxU.png",
                                "格萊天漾大飯店\n\nWanhua Dist., Bangka Blvd, No. 101")

    elif callback.data == "traffinfo_mrt":
        buttons = [{
            "回交通方式": "traffinfo"
        }]

        media = InputMediaPhoto("https://i.imgur.com/PCAgSF7.png",
                                "捷運板南線 龍山寺\n捷運站 2 號出口出站，步行約 5 分鐘")

    elif callback.data == "traffinfo_tra":
        buttons = [{
            "回交通方式": "traffinfo"
        }]

        media = InputMediaPhoto("https://i.imgur.com/PCAgSF7.png",
                                "萬華火車站\n出站步行約 1 分鐘")

    elif callback.data == "traffinfo_bus":
        buttons = [{
            "回交通方式": "traffinfo"
        }]

        media = InputMediaPhoto("https://i.imgur.com/FmMu5j2.png",
                                "捷運龍山寺站\n1、201、231、234、245、264、265、265夜、265區、310、38、38區、49、568、651、656、658、701、705、907、985、藍28、仁愛幹線\n\n萬華車站【康定路】\n201、202、205、49、601、62、985、藍29\n\n萬華車站【艋舺大道】\n1820、1821、1825、1915、667、9089、956")

    elif callback.data == "traffinfo_car":
        buttons = [{
            "回交通方式": "traffinfo"
        }]

        media = InputMediaPhoto("https://i.imgur.com/QNzEtiy.png",
                                "國道一號 25 出口 [台北] 下交流道→重慶北路→右轉市民大道→左轉塔城街→接中華路→直行至艋舺大道\n\n萬華車站地下停車場：西園路一段306巷 (距離10公尺)\n凱達大飯店附屬停車場：艋舺大道 260 號 (距離400公尺)\n台鐵行李房停車場：艋舺大道 101 號 (距離10公尺)")

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
