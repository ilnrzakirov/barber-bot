from decouple import config
from sqlalchemy.engine import URL

from db import (
    asinc_engine,
    get_session_maker,
)

BOT_TOKEN = config("BOT_TOKEN")
postgres_url = URL.create(
    "postgresql+asyncpg",
    username="postgres",
    password="postgres",
    port=5432,
    database="postgres",
    host="localhost",
)
admin_list = [158572669]
owner = config("OWNER")

async_engine = asinc_engine(postgres_url)
session_maker = get_session_maker(async_engine)  # noqa f841
