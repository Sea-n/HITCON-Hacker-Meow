import logging
from typing import List, TextIO

log: logging.Logger = logging.getLogger(__name__)

import json
import os

FILE_PATH: str = os.getcwd() + "/users.json"


def get_whitelist() -> List[int]:
    try:
        f: TextIO = open(FILE_PATH, "r")
        f.close()

    except FileNotFoundError:
        with open(FILE_PATH, "w") as f:
            f.write("{\"users\":[]}")

    finally:
        with open(FILE_PATH, "r") as f:
            s: str = f.read()

    file: dict = json.loads(s)
    users: list = file['users']
    return users


def add_whitelist(uid: int) -> None:
    users: list = get_whitelist()

    data: dict = {'users': []}

    if uid not in users:
        users.append(uid)
        data['users'] = sorted(users)

    string: str = json.dumps(data)

    with open(FILE_PATH, "w") as f:
        f.write(string)
