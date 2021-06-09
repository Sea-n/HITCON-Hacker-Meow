import json
import logging
import os
from typing import List, TextIO

log: logging.Logger = logging.getLogger(__name__)

FILE_PATH: str = os.getcwd() + "/users.json"


def get_whitelist() -> List[int]:
    if not os.path.exists(FILE_PATH):
        return []

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
