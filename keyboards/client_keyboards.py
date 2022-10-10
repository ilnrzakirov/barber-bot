from datetime import datetime

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from sqlalchemy.future import select

from db.db import (
    HairDay,
    Record,
)
from settings import session_maker

button_get_our_hair_cut = KeyboardButton("/Записатся")
button_location = KeyboardButton("/Месторасположение")
button_feedback = KeyboardButton("/Отзыв")

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_client.add(button_get_our_hair_cut).add(button_location).add(button_feedback)


async def get_open_time(name: str, date: datetime.date):
    """
        Функция создает клавиатуру свободных часов и возвращяет
    :param name: str Имя мастера
    :param date: datetime.date
    :return: ReplyKeyboardMarkup
    """
    time_keyboards = ReplyKeyboardMarkup(resize_keyboard=True)
    session = session_maker()
    open_time = await session.execute(select(HairDay).where(HairDay.master_name == name, HairDay.date == date))
    close_time = await session.execute(select(Record).where(Record.master == name, Record.date == date))
    close_time_list = []
    for time in close_time:
        close_time_list.append(time[0].record_time)
    instance = open_time.scalars().first()
    if instance is None:
        return None
    for time in range(instance.open, instance.close):
        if time in close_time_list:
            continue
        time_keyboards.insert(KeyboardButton(str(time)))
    return time_keyboards
