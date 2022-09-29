from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

import settings

storage = MemoryStorage()

bot = Bot(token=settings.BOT_TOKEN)
dispatcher = Dispatcher(bot, storage=storage)
