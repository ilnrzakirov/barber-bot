from aiogram.utils import executor

from bot_init import dispatcher
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


def main():
    client.register_handlers_client(dispatcher)
    admin.register_handlers_admin(dispatcher)
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
    async_engine = asinc_engine(postgres_url)
    session_maker = get_session_maker(async_engine)  # noqa f841
    proceed_schemas(async_engine, BaseModel.metadata)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
