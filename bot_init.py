from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import Dispatcher
from aioredis import Redis

import settings

storage = MemoryStorage()
redis = Redis()

bot = Bot(token=settings.BOT_TOKEN)
dispatcher = Dispatcher(bot, storage=RedisStorage2())
