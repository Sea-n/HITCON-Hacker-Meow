import logging
from typing import Optional

from bot.functions import get_agenda_by_info, get_agendas_by_room, get_agendas_by_time, get_day_photo, get_day_slots, \
    get_room_name, get_room_photo, get_time_photo, get_time_str
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("agenda") & ~ filters.forwarded)
async def agenda(cli: Client, msg: Message) -> None:
    keyboard = [[
        InlineKeyboardButton(get_room_name("r0"), "agenda_R0"),
    ], [
        InlineKeyboardButton(get_room_name("r1"), "agenda_R1"),
        InlineKeyboardButton(get_room_name("r2"), "agenda_R2"),
        InlineKeyboardButton(get_room_name("r3"), "agenda_R3"),
    ], [
        InlineKeyboardButton(get_room_name("r4"), "agenda_R4"),
    ], [
        InlineKeyboardButton("回主選單", "help"),
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await cli.send_photo(msg.chat.id, "https://i.imgur.com/jDeodyc.jpg",
                         "議程總覽\n"
                         "你想看哪個演講廳", reply_markup=reply_markup)


@Client.on_callback_query(filters.regex('^agenda'))
async def events_callback(cli: Client, callback: CallbackQuery) -> None:
    if callback.data == "agenda":
        keyboard = [[
            InlineKeyboardButton(get_room_name("r0"), "agenda_R0"),
        ], [
            InlineKeyboardButton(get_room_name("r1"), "agenda_R1"),
            InlineKeyboardButton(get_room_name("r2"), "agenda_R2"),
            InlineKeyboardButton(get_room_name("r3"), "agenda_R3"),
        ], [
            InlineKeyboardButton(get_room_name("r4"), "agenda_R4"),
        ], [
            InlineKeyboardButton("Day 1", "agenda_D1"),
            InlineKeyboardButton("Day 2", "agenda_D2"),
        ], [
            InlineKeyboardButton("回主選單", "help")
        ]]

        media = InputMediaPhoto("https://i.imgur.com/jDeodyc.jpg",
                                "議程總覽\n"
                                "你想看哪個演講廳")
    # agenda_{ROOM}_{DAY}{TIME}
    # example: R0, R0_1A, D1, D1A
    else:
        _ = callback.data.split("_")

        if len(_) == 2 and _[1].startswith("R"):
            room: str = _[1]
            agendas: list = get_agendas_by_room(room)

            keyboard: list[list[InlineKeyboardButton]] = []

            agendas.sort(key=lambda x: (x["time"][-1], x["time"][-2]))

            _k: list[InlineKeyboardButton] = []
            prev: Optional[dict] = None

            for agenda in agendas:
                if prev is not None:
                    if not agenda["time"][-1] == prev["time"][-1]:
                        keyboard.append(_k)
                        _k: list[InlineKeyboardButton] = []

                day: str = agenda["time"][-2]
                time: str = agenda["time"][-1]
                _k.append(InlineKeyboardButton(agenda["title"], f"agenda_{room}_{day}{time}"))
                prev: list = agenda

            keyboard.append(_k)
            keyboard.append([InlineKeyboardButton("回議程總覽", "agenda")])

            media = InputMediaPhoto(get_room_photo(room),
                                    f"你想查看 {get_room_name(room)} 的哪一個議程呢")

        elif len(_) == 2 and _[1].startswith("D"):
            # D1, D1A
            para: str = _[1]

            time: Optional[str] = None
            day: str = para[1]

            if not para[-1].isdigit():
                time: str = para[-1]

            if time is None:
                # D1
                keyboard: list[list[InlineKeyboardButton]] = []

                slots: list = get_day_slots(day)

                for _ in slots:
                    tmp: tuple = _.popitem()
                    time_code: str = tmp[0]
                    ranges: dict = tmp[1]

                    keyboard.append(
                        [
                            InlineKeyboardButton(
                                f"{ranges.get('start')} - {ranges.get('end')}",
                                f"agenda_D{day}{time_code}"
                            )
                        ]
                    )

                keyboard.append([
                    InlineKeyboardButton("回議程總覽", "agenda")
                ])
                media = InputMediaPhoto(get_day_photo(day),
                                        f"Day {day} 議程總覽\n"
                                        f"你想查看甚麼時候的議程呢")

            else:
                # D1A
                agendas: list = get_agendas_by_time(day, time)

                keyboard: list[list[InlineKeyboardButton]] = []

                for agenda in agendas:
                    agenda_keyboard: list[InlineKeyboardButton] = [
                        InlineKeyboardButton(agenda["title"], agenda["callback"])
                    ]
                    keyboard.append(agenda_keyboard)

                keyboard.append([InlineKeyboardButton(f"回 Day {day} 議程", f"agenda_D{day}")])

                media = InputMediaPhoto(get_time_photo(day, time),
                                        f"Day {day} {get_time_str(day, time)} 的所有議程\n"
                                        f"你想看哪個議程呢")

        elif len(_) == 3:
            # R0_1A
            _, room, time = _
            day = time[0]
            time = time[-1]

            agenda = get_agenda_by_info(room, day, time)

            keyboard: list[list[InlineKeyboardButton]] = []

            for link_name in agenda["links"]:
                keyboard.append([InlineKeyboardButton(link_name, url=agenda["links"].get(link_name))])

            keyboard.append([
                InlineKeyboardButton(f"回到 {get_room_name(room)} 議程", f"agenda_{room}"),
                InlineKeyboardButton("同時段議程", f"agenda_D{day}{time}"),
            ])

            media = InputMediaPhoto(agenda["photo"], agenda["description"])

        else:
            keyboard = []
            media = None

    await cli.edit_message_media(callback.message.chat.id,
                                 callback.message.message_id,
                                 media=media,
                                 reply_markup=InlineKeyboardMarkup(keyboard))

    await cli.answer_callback_query(callback.id)
