from aiogram import (
    Dispatcher,
    types,
)
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import (
    State,
    StatesGroup,
)
from loguru import logger

from db.db import Master
from settings import session_maker


class OpenHairDay(StatesGroup):
    date = State()
    master = State()
    open_time = State()
    close_time = State()
    dinner = State()


class HairMaster(StatesGroup):
    name = State()


async def open_hair_day(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username}")
    await OpenHairDay.date.set()
    await message.answer("Напиши дату в формате ДД.ММ.ГГГГ")


async def init_hair_day(message: types.Message, state: FSMContext):
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["date"] = message.text
    await OpenHairDay.next()
    await message.answer("Выбери мастера")


async def init_master(message: types.Message, state: FSMContext):
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["master"] = message.text
    await OpenHairDay.next()
    await message.answer("Во сколько начинается рабочий день?")


async def init_open_time(message: types.Message, state: FSMContext):
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["open_time"] = message.text
    await OpenHairDay.next()
    await message.answer("Во сколько заканчивается рабочий день?")


async def init_close_time(message: types.Message, state: FSMContext):
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["close_time"] = message.text
    await OpenHairDay.next()
    await message.answer("Во сколько обед?")


async def init_dinner_time(message: types.Message, state: FSMContext):
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["dinner"] = message.text
    # day = HairDay()
    await message.answer("Спасибо, можно записываться")


async def create_master(message: types.Message):
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    await HairMaster.name.set()
    await message.answer("Как зовут мастера?")


async def init_master_name(message: types.Message, state: FSMContext):
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["name"] = message.text
    master = Master(name=message.text)
    session = session_maker()
    session.add(master)
    await session.commit()
    await message.answer("Мастер добавлен")


def register_handlers_admin(dispatcher: Dispatcher):
    dispatcher.register_message_handler(open_hair_day, commands=["open_day"], state=None)
    dispatcher.register_message_handler(init_hair_day, state=OpenHairDay.date)
    dispatcher.register_message_handler(create_master, commands=["add_master"], state=None)
    dispatcher.register_message_handler(init_master_name, state=HairMaster.name)
    dispatcher.register_message_handler(init_master, state=OpenHairDay.master)
    dispatcher.register_message_handler(init_open_time, state=OpenHairDay.open_time)
    dispatcher.register_message_handler(init_close_time, state=OpenHairDay.close_time)
    dispatcher.register_message_handler(init_dinner_time, state=OpenHairDay.dinner)
