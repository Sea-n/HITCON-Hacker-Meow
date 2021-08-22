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


def get_agenda_by_room(room: str) -> dict:
    file: dict = _get_data()
    agendas: dict = file.get(room)

    list_agenda: list = []
    for _ in agendas:
        for agenda in agendas.get(_):
            agenda["day"] = _
            list_agenda.append(agenda)

    agendas: dict = {agenda["time_slot"]: [] for agenda in list_agenda}

    for agenda in list_agenda:
        agendas[agenda["time_slot"]].append(agenda)
        agendas[agenda["time_slot"]].sort(key=lambda x: x["day"])

    return agendas


def get_agenda_by_info(room, day, time) -> dict:
    file: dict = _get_data()
    s: list = file.get(room).get(day)
    for _ in s:
        if _["time_slot"] == time:
            return _


def get_agenda_by_time(time: str, day: str) -> list:
    data: dict = _get_data()
    agendas: list[dict] = []

    for _ in data:
        for agenda in data.get(_).get(day):
            if agenda["time_slot"] == time:
                agenda["callback"] = f"agenda_{_}_{day}{time}"
                agendas.append(agenda)
    return agendas
