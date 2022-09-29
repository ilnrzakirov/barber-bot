from aiogram import (
    Dispatcher,
    types,
)
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


def register_handlers_client(dispatcher: Dispatcher):
    dispatcher.register_message_handler(open_hair_day, commands=["Открыть запись"], state=None)
