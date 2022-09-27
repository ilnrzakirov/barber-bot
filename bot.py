from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import settings
from loguru import logger

logger.add("log.log", format="{time}, {level}, {message}", level="INFO", encoding="UTF-8")

bot = Bot(token=settings.BOT_TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler()
async def echo(message: types.Message):
    await message.answer("Hello")


logger.info("Бот запущен")
executor.start_polling(dispatcher, skip_updates=True)
