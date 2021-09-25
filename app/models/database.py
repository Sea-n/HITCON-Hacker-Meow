import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import registry, sessionmaker
from sqlalchemy.orm.decl_api import declarative_base


class Database:
    engine: Engine = create_engine(os.getenv("SQLITE_URI"), echo=True, future=True)
    mapper_registry: registry = registry()
    base: declarative_base = mapper_registry.generate_base()
    metadata = base.metadata

    session = sessionmaker(engine)

    def init(self):
        self.metadata.create_all(self.engine)


db: Database = Database()
