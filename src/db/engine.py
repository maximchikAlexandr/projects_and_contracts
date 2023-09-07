import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, event
from sqlalchemy.engine import Engine

load_dotenv(".env")


def set_timezone(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET timezone = 'Europe/Minsk';")


class EngineDB:
    url_obj = URL.create(
        "postgresql",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("POSTGRES_DB"),
    )
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = create_engine(url=cls.url_obj)
            event.listen(cls.__instance, "connect", set_timezone)
        return cls.__instance
