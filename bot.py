from aiogram.utils import executor

from bot_init import dispatcher
from handlers import client
from utils.loger_init import logger


@logger.catch()
async def on_startup(_):
    logger.info("Бот запущен")

client.register_handlers_client(dispatcher)

executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
