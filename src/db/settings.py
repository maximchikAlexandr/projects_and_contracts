import logging
import os

from dotenv import load_dotenv
from psycopg2.extensions import connection, cursor
from sqlalchemy import URL, create_engine, event
from sqlalchemy.engine.base import Engine
from sqlalchemy.pool.base import _ConnectionRecord

load_dotenv(".env")


log_level: str = os.getenv("SQLALCHEMY_LOG_LEVEL")
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(getattr(logging, log_level))


def set_timezone(
    dbapi_connection: connection, connection_record: _ConnectionRecord
) -> None:
    cursor_obj: cursor = dbapi_connection.cursor()
    cursor_obj.execute("SET timezone = 'Europe/Minsk';")


class EngineDB:
    url_obj: URL = URL.create(
        "postgresql",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("POSTGRES_DB"),
    )
    __instance = None

    def __new__(cls) -> Engine:
        if cls.__instance is None:
            cls.__instance: Engine = create_engine(url=cls.url_obj)
            event.listen(cls.__instance, "connect", set_timezone)
        return cls.__instance
