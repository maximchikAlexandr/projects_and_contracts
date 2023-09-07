from sqlalchemy import URL, create_engine

import os
from dotenv import load_dotenv

load_dotenv('.env')


class EngineDB:
    url_obj = URL.create(
        "postgresql",
        username=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('POSTGRES_DB'),
    )
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = create_engine(url=cls.url_obj)
        return cls.__instance
