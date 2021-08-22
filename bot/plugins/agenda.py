import logging

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message

from bot.functions import get_agenda_by_info, get_agenda_by_room, get_agenda_by_time

log: logging.Logger = logging.getLogger(__name__)


def get_time_str(day, time) -> str:
    if day == "1":
        table = {
            "A": "11:00 - 11:50",
            "B": "13:00 - 13:50",
            "C": "14:00 - 14:50",
            "D": "15:30 - 16:20",
            "E": "16:30 - 17:20",
        }
        return table[time]
    else:
        table = {
            "A": "09:20 - 10:10",
            "B": "10:20 - 11:10",
            "C": "11:20 - 12:10",
            "D": "13:50 - 14:40",
            "E": "14:50 - 15:40",
        }
        return table[time]


@Client.on_message(filters.command("agenda") & ~ filters.forwarded)
async def agenda(cli: Client, msg: Message) -> None:
    keyboard = [[
        InlineKeyboardButton("Track 01", "agenda_R0"),
    ], [
        InlineKeyboardButton("Track 02", "agenda_R1"),
        InlineKeyboardButton("Track 03", "agenda_R2"),
        InlineKeyboardButton("Track 04", "agenda_R3"),
        InlineKeyboardButton("Track 05", "agenda_R4"),
    ], [
        InlineKeyboardButton("回主選單", "help")
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await cli.send_photo(msg.chat.id, "https://i.imgur.com/jDeodyc.jpg",
                         "議程總覽\n你想看哪個演講廳", reply_markup=reply_markup)


@Client.on_callback_query(filters.regex('^agenda'))
async def events_callback(cli: Client, callback: CallbackQuery) -> None:
    if callback.data == "agenda":
        keyboard = [[
            InlineKeyboardButton("Track 01", "agenda_R0"),
            InlineKeyboardButton("Track 02", "agenda_R1"),
            InlineKeyboardButton("Track 03", "agenda_R2"),
            InlineKeyboardButton("Track 04", "agenda_R3"),
            InlineKeyboardButton("Track 05", "agenda_R4"),
        ], [
            InlineKeyboardButton("Day 1", "agenda_D1"),
            InlineKeyboardButton("Day 2", "agenda_D2"),
        ], [
            InlineKeyboardButton("回主選單", "help")
        ]]

        media = InputMediaPhoto("https://i.imgur.com/jDeodyc.jpg",
                                "議程總覽\n你想看哪個演講廳")
    # agenda_{ROOM}_{DAY}{TIME}
    # example: R0, R0_1A, D1, D1A
    else:
        _ = callback.data.split("_")
        if len(_) == 2:
            # test first char D or R
            room_or_day: str = _[1]

            if room_or_day.startswith("R"):
                room: str = room_or_day
                agendas: dict = get_agenda_by_room(room)

                keyboard: list[list[InlineKeyboardButton]] = []

                for _ in agendas:
                    agenda_keyboard: list[InlineKeyboardButton] = []
                    for agenda in agendas.get(_):
                        agenda_keyboard.append(
                            InlineKeyboardButton(agenda["topic"], f"agenda_{room}_D{agenda['day']}{_}")
                        )
                    keyboard.append(agenda_keyboard)

                keyboard.append([InlineKeyboardButton("回議程總覽", "agenda")])

                media = InputMediaPhoto("https://i.imgur.com/SsAfqPg.png",
                                        "來個貓貓照")

            elif room_or_day.startswith("D"):

                if room_or_day == "D1":
                    keyboard = [[
                        InlineKeyboardButton(get_time_str("1", "A"), "agenda_D1A"),
                        InlineKeyboardButton(get_time_str("1", "B"), "agenda_D1B"),
                    ], [
                        InlineKeyboardButton(get_time_str("1", "C"), "agenda_D1C"),
                    ], [
                        InlineKeyboardButton(get_time_str("1", "D"), "agenda_D1D"),
                        InlineKeyboardButton(get_time_str("1", "E"), "agenda_D1E"),
                    ], [
                        InlineKeyboardButton("回議程總覽", "agenda")
                    ]]

                    media = InputMediaPhoto("https://i.imgur.com/SsAfqPg.png",
                                            "Day 1 議程總覽\n請選擇時段")

                elif room_or_day == "D2":
                    keyboard = [[
                        InlineKeyboardButton(get_time_str("2", "A"), "agenda_D2A"),
                        InlineKeyboardButton(get_time_str("2", "B"), "agenda_D2B"),
                    ], [
                        InlineKeyboardButton(get_time_str("2", "C"), "agenda_D2C"),
                    ], [
                        InlineKeyboardButton(get_time_str("2", "D"), "agenda_D2D"),
                        InlineKeyboardButton(get_time_str("2", "E"), "agenda_D2E"),
                    ], [
                        InlineKeyboardButton("回議程總覽", "agenda")
                    ]]

                    media = InputMediaPhoto("https://i.imgur.com/T2WWUla.png",
                                            "Day 2 議程總覽\n請選擇時段")

                else:
                    day: str = room_or_day[1]
                    time: str = room_or_day[-1]

                    agendas: list = get_agenda_by_time(time, day)

                    keyboard: list[list[InlineKeyboardButton]] = []

                    for agenda in agendas:
                        agenda_keyboard: list[InlineKeyboardButton] = []
                        agenda_keyboard.append(
                            InlineKeyboardButton(agenda["topic"], agenda["callback"])
                        )
                        keyboard.append(agenda_keyboard)

                    keyboard.append([InlineKeyboardButton(f"回 Day {day} 議程", f"agenda_D{day}")])

                    media = InputMediaPhoto("https://i.imgur.com/IicQq8u.png",
                                            f"Day {day} {get_time_str(day, time)} 議程\n"
                                            "請選擇場次")
        else:
            # multiple variables
            _, room, time = _
            day = time[1]
            time = time[-1]

            agenda = get_agenda_by_info(room, day, time)

            keyboard: list[list[InlineKeyboardButton]] = []

            for link in agenda["links"]:
                keyboard.append([InlineKeyboardButton(link, url=agenda["links"].get(link))])

            keyboard.append([
                InlineKeyboardButton("回到上一頁", f"agenda_{room}"),
                InlineKeyboardButton("同時段議程", f"agenda_D{day}{time}"),
            ])

            media = InputMediaPhoto(agenda["photo_link"], agenda["description"])

    await cli.edit_message_media(callback.message.chat.id,
                                 callback.message.message_id,
                                 media=media,
                                 reply_markup=InlineKeyboardMarkup(keyboard))

    await cli.answer_callback_query(callback.id)
