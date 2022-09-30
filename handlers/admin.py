from aiogram import (
    Dispatcher,
    types,
)
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import (
    State,
    StatesGroup,
)


class OpenHairDay(StatesGroup):
    date = State()
    master = State()
    open_time = State()
    close_time = State()
    dinner = State()


async def open_hair_day(message: types.Message):
    await OpenHairDay.date.set()
    await message.answer("Напиши дату в формате ДД.ММ.ГГГГ")


async def init_hair_day(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["date"] = message.text
    await OpenHairDay.next()
    await message.answer("Выбери мастера")


def register_handlers_admin(dispatcher: Dispatcher):
    dispatcher.register_message_handler(open_hair_day, commands=["open_day"], state=None)
    dispatcher.register_message_handler(init_hair_day, state=OpenHairDay.date)
