from decouple import config
from sqlalchemy.engine import URL

BOT_TOKEN = config("BOT_TOKEN")
postgres_url = URL.create(
    "postgresql+asyncpg",
    username="postgres",
    password="postgres",
    port=5432,
    database="postgres",
    host="localhost",
)
