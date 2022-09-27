from aiogram import Bot, types
from aiogram.dispatcher import dispatcher
from aiogram.utils import executor
import settings
from loguru import logger

logger.add("log.log", format="{time}, {level}, {message}", level="INFO", encoding="UTF-8")

