import asyncio

from aiogram.utils import executor  # noqa F401

from bot_init import (
    bot,
    dispatcher,
)
from handlers import (
    admin,
    client,
)
from utils.loger_init import logger


@logger.catch()
async def on_startup(_):
    logger.info("Бот запущен")


@logger.catch()
async def main():
    client.register_handlers_client(dispatcher)
    admin.register_handlers_admin(dispatcher)
    # await proceed_schemas(async_engine, BaseModel.metadata)
    logger.info("Бот запущен")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        logger.error(error)
