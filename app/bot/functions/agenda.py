import json
import logging
import os

log: logging.Logger = logging.getLogger(__name__)

FILE_PATH: str = os.getcwd() + "/agenda.json"


def _get_data() -> dict:
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        s: str = f.read()

    data: dict = json.loads(s)
    return data


def get_room_name(room: str) -> str:
    data: dict = _get_data()
    rooms: dict = data.get("rooms")
    room_name: str = rooms.get(room.lower()).get("name")

    return room_name


def get_room_photo(room: str) -> str:
    data: dict = _get_data()
    rooms: dict = data.get("rooms")
    room_name: str = rooms.get(room.lower()).get("photo")

    return room_name


def get_time_str(day, time) -> str:
    slots = get_day_slots(day)

    for _ in slots:
        tmp = _.popitem()
        if tmp[0] == time:
            return f"{tmp[1].get('start')} - {tmp[1].get('end')}"


def get_time_photo(day, time) -> str:
    slots = get_day_slots(day)

    for _ in slots:
        tmp = _.popitem()
        if tmp[0] == time:
            return f"{tmp[1].get('photo')}"


def get_day_slots(day: str) -> list[dict]:
    data: dict = _get_data()
    times: dict = data.get("times")

    return times.get(f"day{day}").get("slots")


def get_day_photo(day: str) -> str:
    data: dict = _get_data()
    time: dict = data.get("times")
    photo: str = time.get(f"day{day}").get("photo")

    return photo


def get_agendas_by_room(room: str) -> list[dict[str, str]]:
    data: dict = _get_data()
    agendas: list = data.get("agendas")

    list_agenda: list = []
    for agenda in agendas:
        if agenda.get("room") == room.lower():
            list_agenda.append(agenda)

    list_agenda.sort(key=lambda x: (x["time"][-2], x["time"][-1]))

    return list_agenda


def get_agenda_by_info(room, day, time) -> dict:
    data: dict = _get_data()

    agendas: list[dict] = data.get("agendas")

    for _ in agendas:
        if _["time"] == f"day{day}{time}" and _["room"] == room.lower():
            return _


def get_agendas_by_time(day: str, time: str) -> list:
    data: dict = _get_data()
    agendas: list = data.get("agendas")

    list_agenda: list = []
    for agenda in agendas:
        if agenda["time"] == f"day{day}{time}":
            agenda["callback"] = f"agenda_{agenda['room'].upper()}_{day}{time}"
            list_agenda.append(agenda)

    return list_agenda
