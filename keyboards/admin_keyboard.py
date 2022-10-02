from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from sqlalchemy.future import select

from db.db import Master
from settings import session_maker

button_open_day = KeyboardButton("/open_day")
button_add_master = KeyboardButton("/add_master")

keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_admin.add(button_open_day).add(button_add_master)


async def get_master_keyboard():
    session = session_maker()
    master_list = await session.execute(select(Master))
    keyboard_master = ReplyKeyboardMarkup(resize_keyboard=True)
    for master in master_list:
        keyboard_master.add(KeyboardButton(master[0].name))
    return keyboard_master
