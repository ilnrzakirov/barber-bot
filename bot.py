import asyncio

from aiogram.utils import executor  # noqa F401

from bot_init import (
    bot,
    dispatcher,
)
from db import (
    BaseModel,
    asinc_engine,
    get_session_maker,
    proceed_schemas,
)
from handlers import (
    admin,
    client,
)
from settings import postgres_url
from utils.loger_init import logger


@logger.catch()
async def on_startup(_):
    logger.info("Бот запущен")


@logger.catch()
async def main():
    client.register_handlers_client(dispatcher)
    admin.register_handlers_admin(dispatcher)
    async_engine = asinc_engine(postgres_url)
    session_maker = get_session_maker(async_engine)  # noqa f841
    await proceed_schemas(async_engine, BaseModel.metadata)
    logger.info("Бот запущен")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        print(error)
