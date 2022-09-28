from aiogram import Bot
from aiogram.dispatcher import Dispatcher

import settings

bot = Bot(token=settings.BOT_TOKEN)
dispatcher = Dispatcher(bot)
