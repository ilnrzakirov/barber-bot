from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from sqlalchemy.future import select

from db.db import Master
from settings import session_maker

button_open_day = KeyboardButton("/open_day")
button_add_master = KeyboardButton("/add_master")
button_delete_master = KeyboardButton("/delete_master")

keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_admin.row(button_open_day, button_add_master, button_delete_master)


async def get_master_keyboard():
    session = session_maker()
    master_list = await session.execute(select(Master))
    keyboard_master = ReplyKeyboardMarkup(resize_keyboard=True)
    for master in master_list:
        keyboard_master.add(KeyboardButton(master[0].name))
    return keyboard_master


async def delete_master_db(name: str):
    session = session_maker()
    master = await session.execute(select(Master).where(Master.name == name))
    instanse = master.scalars().first()
    if instanse is None:
        return None
    await session.delete(instanse)
    await session.commit()
    return True
