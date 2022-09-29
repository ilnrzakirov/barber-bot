from aiogram import (
    Dispatcher,
    types,
)
from loguru import logger

from keyboards.client_keyboards import keyboard_client


@logger.catch()
async def start(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username}")
    await message.answer(
        "Парикма́херская — это предприятие, занимающееся предоставлением "
        "услуг для населения по уходу за волосами (стрижка, завивка, создание причёски,"
        " окрашивание, мелирование и другие виды работ с красителями, стрижка огнём, "
        "бритьё и стрижка бород и усов и др.) в оборудованном специально для этого помещении.",
        reply_markup=keyboard_client,
    )


@logger.catch()
async def location(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username}")
    await message.answer("Здесь будет изображение карты")


def register_handlers_client(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start, commands=["start", "help"])
    dispatcher.register_message_handler(location, commands=["Месторасположение"])
