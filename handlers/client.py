from aiogram import (
    Dispatcher,
    types,
)
from loguru import logger

from keyboards.admin_keyboard import (
    get_admin_list,
    keyboard_admin,
    owner_keyboard,
)
from keyboards.client_keyboards import keyboard_client
from settings import owner


@logger.catch()
async def start(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username} - id {message.from_user.id}")
    admin_list = await get_admin_list()
    if message.from_user.id == int(owner):
        keyboard = owner_keyboard
    elif message.from_user.id in admin_list:
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
