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
    Feedback,
    Record,
)
from keyboards.admin_keyboard import (
    get_admin_list,
    get_master_keyboard,
    keyboard_admin,
    owner_keyboard,
)
from keyboards.client_keyboards import (
    get_open_time,
    keyboard_client,
)
from settings import (
    owner,
    session_maker,
)


class RecordState(StatesGroup):
    master = State()
    date = State()
    record_time = State()


class FeedbackState(StatesGroup):
    master = State()
    feedback = State()


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


@logger.catch()
async def recording(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username}")
    await RecordState.master.set()
    keyboard = await get_master_keyboard()
    await message.answer("Выбери мастера", reply_markup=keyboard)


@logger.catch()
async def set_master(message: types.Message, state: FSMContext):
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["master"] = message.text
    await RecordState.next()
    await message.answer("Напиши дату в формате ДД.ММ.ГГГГ")


@logger.catch()
async def set_record_date(message: types.Message, state: FSMContext):
    try:
        logger.info(f"Получены данные {message.text} от {message.from_user.username}")
        async with state.proxy() as data:
            data["date"] = message.text
        date = datetime.datetime.strptime(data["date"], "%d.%m.%Y")
        open_date_keyboard = await get_open_time(data["master"], date.date())
        await RecordState.next()
        if open_date_keyboard is None:
            await message.answer("Свободных мест нет", reply_markup=keyboard_client)
        else:
            await message.answer("Выберите время", reply_markup=open_date_keyboard)
    except ValueError:
        await state.finish()
        await message.answer("Произошла ошибка, попробуйте позже", reply_markup=keyboard_client)


@logger.catch()
async def set_record_time(message: types.Message, state: FSMContext):
    try:
        logger.info(f"Получены данные {message.text} от {message.from_user.username}")
        async with state.proxy() as data:
            data["record_time"] = message.text
        date = datetime.datetime.strptime(data["date"], "%d.%m.%Y")
        session = session_maker()
        record = Record(data["master"], int(data["record_time"]), date.date())
        session.add(record)
        await session.commit()
        await state.finish()
        await message.answer("Спасибо, записал", reply_markup=keyboard_client)
    except ValueError as error:
        print(error)
        await state.finish()
        await message.answer("Произошла ошибка", reply_markup=keyboard_client)


@logger.catch()
async def add_feedback(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username}")
    await FeedbackState.master.set()
    keyboard = await get_master_keyboard()
    await message.answer("Выбери мастера", reply_markup=keyboard)


@logger.catch()
async def set_master_feedback(message: types.Message, state: FSMContext):
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["master"] = message.text
    await FeedbackState.next()
    await message.answer("Текст отзыва")


@logger.catch()
async def set_feedback_text(message: types.Message, state: FSMContext):
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["feedback"] = message.text
    session = session_maker()
    feedback = Feedback(master=data["master"], message=data["feedback"])
    session.add(feedback)
    await session.commit()
    await state.finish()
    await message.answer("Спасибо за отзыв")


def register_handlers_client(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start, commands=["start", "help"])
    dispatcher.register_message_handler(location, commands=["Месторасположение"])
    dispatcher.register_message_handler(recording, commands=["Записатся"], state=None)
    dispatcher.register_message_handler(set_master, state=RecordState.master)
    dispatcher.register_message_handler(set_record_date, state=RecordState.date)
    dispatcher.register_message_handler(set_record_time, state=RecordState.record_time)
    dispatcher.register_message_handler(add_feedback, commands=["Отзыв"], state=None)
    dispatcher.register_message_handler(set_master_feedback, state=FeedbackState.master)
    dispatcher.register_message_handler(set_feedback_text, state=FeedbackState.feedback)
