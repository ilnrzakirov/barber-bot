import datetime

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

from db.db import (
    HairDay,
    Master,
)
from keyboards.admin_keyboard import (
    delete_master_db,
    get_all_feedback,
    get_master_keyboard,
    keyboard_admin,
)
from settings import session_maker


class OpenHairDay(StatesGroup):
    """
        Стейт для открытия рабочего дня
    """
    date = State()
    master = State()
    open_time = State()
    close_time = State()
    dinner = State()


class HairMaster(StatesGroup):
    """
        Стейт мастера
    """
    name = State()


class DeleteMasterState(StatesGroup):
    name = State()


async def open_hair_day(message: types.Message):
    """
        Корутина добавления рабочего дня. Принимает дату
    """
    logger.info(f"Получена команда {message.text} от {message.from_user.username}")
    await OpenHairDay.date.set()
    await message.answer("Напиши дату в формате ДД.ММ.ГГГГ")


async def init_hair_day(message: types.Message, state: FSMContext):
    """
        Корутина доавбления мастера в Стейт рабочего дня
    """
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["date"] = message.text
    await OpenHairDay.next()
    master_keyboard = await get_master_keyboard()
    await message.answer("Выбери мастера", reply_markup=master_keyboard)


async def init_master(message: types.Message, state: FSMContext):
    """
        Корутина записывает данные о мастере
    :param message: Message
    :param state: FSMContext
    :return: message.answer
    """
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["master"] = message.text
    await OpenHairDay.next()
    await message.answer("Во сколько начинается рабочий день?")


async def init_open_time(message: types.Message, state: FSMContext):
    """
        Корутина записывет данные о начале рабочего дня
    :param message: Message
    :param state: FSMContext
    :return: message.answer
    """
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["open_time"] = message.text
    await OpenHairDay.next()
    await message.answer("Во сколько заканчивается рабочий день?")


async def init_close_time(message: types.Message, state: FSMContext):
    """
        Корутина записывает данные о времени окончания рабочего дня
    :param message: Message
    :param state: FSMContext
    :return: message.answer
    """
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["close_time"] = message.text
    await OpenHairDay.next()
    await message.answer("Во сколько обед?")


async def init_dinner_time(message: types.Message, state: FSMContext):
    """
        Корутина записывает данные о времени обеда. Записывает данные о дне в БД и закрывает стейт
    :param message: Message
    :param state: FSMContext
    :return: message.answer
    """
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["dinner"] = message.text
    date = datetime.datetime.strptime(data["date"], "%d.%m.%Y")
    day = HairDay(
        date.date(),
        data["master"],
        int(data["open_time"]),
        int(data["close_time"]),
        int(data["dinner"]),
    )
    session = session_maker()
    session.add(day)
    await state.finish()
    await session.commit()
    await message.answer("Спасибо, можно записываться")


async def create_master(message: types.Message):
    """
        Корутина создает мастера
    :param message: Message
    :return: Message.answer
    """
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    await HairMaster.name.set()
    await message.answer("Как зовут мастера?")


async def init_master_name(message: types.Message, state: FSMContext):
    """
        Корутина принимает имя мастера и записывает в БД. Закрывает стейт
    :param message: Message
    :param state: FSMContext
    :return: Message.answer
    """
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["name"] = message.text
    master = Master(name=message.text)
    session = session_maker()
    session.add(master)
    await session.commit()
    await state.finish()
    await message.answer("Мастер добавлен", reply_markup=keyboard_admin)


async def delete_master(message: types.Message):
    """
        Корутина для удаления мастера
    :param message: Message
    :return: reply_markup
    """
    logger.info(f"Получена команда {message.text} от {message.from_user.username}")
    master_keyboard = await get_master_keyboard()
    await DeleteMasterState.name.set()
    await message.answer("Выберите мастера", reply_markup=master_keyboard)


async def run_delete(message: types.Message, state: FSMContext):
    """
        Корутина принимает имя мастера и удалет из БД
    :param message: Message
    :param state: FSMContext
    :return: reply_markup
    """
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["name"] = message.text
    status = await delete_master_db(data["name"])
    await state.finish()
    if status:
        await message.answer("Мастер успешно удален", reply_markup=keyboard_admin)
    else:
        await message.answer("Нет такого мастера", reply_markup=keyboard_admin)


async def get_feedbacks(message: types.Message):
    """
        Корутна для просмотра отзывов
    :param message: Message
    :return: Message.answer
    """
    logger.info(f"Получена команда {message.text} от {message.from_user.username}")
    msg = await get_all_feedback()
    await message.answer(msg, reply_markup=keyboard_admin)


def register_handlers_admin(dispatcher: Dispatcher):
    """
        Функция для регистрации хендлеров
    :param dispatcher: Dispatcher
    :return: Хендлер
    """
    dispatcher.register_message_handler(open_hair_day, commands=["open_day"], state=None)
    dispatcher.register_message_handler(init_hair_day, state=OpenHairDay.date)
    dispatcher.register_message_handler(create_master, commands=["add_master"], state=None)
    dispatcher.register_message_handler(init_master_name, state=HairMaster.name)
    dispatcher.register_message_handler(init_master, state=OpenHairDay.master)
    dispatcher.register_message_handler(init_open_time, state=OpenHairDay.open_time)
    dispatcher.register_message_handler(init_close_time, state=OpenHairDay.close_time)
    dispatcher.register_message_handler(init_dinner_time, state=OpenHairDay.dinner)
    dispatcher.register_message_handler(delete_master, commands=["delete_master"], state=None)
    dispatcher.register_message_handler(run_delete, state=DeleteMasterState.name)
    dispatcher.register_message_handler(get_feedbacks, commands=["feedbacks"])
