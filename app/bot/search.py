import logging
import os

import requests
from jieba.analyse import ChineseAnalyzer
from whoosh.fields import ID, Schema, TEXT
from whoosh.index import create_in
from whoosh.qparser import MultifieldParser
from whoosh.searching import Results

log: logging.Logger = logging.getLogger(__name__)
SESSION_JSON: str = "https://hitcon.org/2021/speaker/session.json"

schema: Schema = Schema(
    id=ID(stored=True),
    type=ID(stored=True),
    room=ID(stored=True),
    start=ID(stored=True),
    end=ID(stored=True),
    qa=ID(stored=True),
    slide=ID(stored=True),
    title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
    content=TEXT(stored=True, analyzer=ChineseAnalyzer())
)


class Search:
    def __init__(self):
        # init writers
        _index_dir: str = "_index_"
        if not os.path.exists(_index_dir):
            os.mkdir(_index_dir)
        self._ix = create_in(_index_dir, schema)

        _r: requests = requests.get(SESSION_JSON)
        if _r.status_code != 200:
            raise ConnectionError("Can not get the session json, is the bot in offline mode?")
        _data: dict = _r.json()

        _writer = self._ix.writer()
        for _ in _data["sessions"]:
            _writer.add_document(
                id=_["id"],
                type=_["type"],
                room=_["room"],
                start=_["start"],
                end=_["end"],
                qa=_["qa"],
                slide=_["slide"],
                title=_["zh"]["title"],
                content=_["zh"]["description"]
            )
        _writer.commit()

    def search(self, target: str) -> Results:
        """Search session title and description if match the target."""
        searcher = self._ix.searcher()
        parser = MultifieldParser(["title", "content"], schema=schema)
        return searcher.search(parser.parse(target))
