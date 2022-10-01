from aiogram import (
    Dispatcher,
    types,
)
from loguru import logger

from keyboards.admin_keyboard import keyboard_admin
from keyboards.client_keyboards import keyboard_client
from settings import admin_list


@logger.catch()
async def start(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username} - id {message.from_user.id}")
    if message.from_user.id in admin_list:
        keyboard = keyboard_admin
    else:
        keyboard = keyboard_client
    await message.answer(
        f"Привет {message.from_user.first_name}",
        reply_markup=keyboard,
    )


@logger.catch()
async def location(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username}")
    await message.answer("Здесь будет изображение карты")


def register_handlers_client(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start, commands=["start", "help"])
    dispatcher.register_message_handler(location, commands=["Месторасположение"])
