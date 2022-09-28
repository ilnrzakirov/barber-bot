from aiogram import (
    Bot,
    types,
)
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from loguru import logger

import settings

logger.add("log.log", format="{time}, {level}, {message}", level="INFO", encoding="UTF-8")

bot = Bot(token=settings.BOT_TOKEN)
dispatcher = Dispatcher(bot)


@logger.catch()
@dispatcher.message_handler(commands=["start", "help"])
async def echo(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username}")
    await message.answer("Hello")


logger.info("Бот запущен")
executor.start_polling(dispatcher, skip_updates=True)
