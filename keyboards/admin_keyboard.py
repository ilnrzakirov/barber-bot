from typing import List

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from sqlalchemy.future import select

from db.db import (
    Admin,
    Feedback,
    Master,
)
from settings import session_maker

button_open_day = KeyboardButton("/open_day")
button_add_master = KeyboardButton("/add_master")
button_delete_master = KeyboardButton("/delete_master")
button_see_feedback = KeyboardButton("/feedbacks")
add_administrator_button = KeyboardButton("/add_admin")
delete_administrator_button = KeyboardButton("/delete_admin")

keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_admin.row(button_open_day, button_add_master, button_delete_master).add(button_see_feedback)

owner_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
owner_keyboard.add(add_administrator_button, delete_administrator_button)


async def get_master_keyboard():
    """
        Функция создает и возвращяет клавиатуру с именами мастеров
    :return: ReplyKeyboardMarkup
    """
    session = session_maker()
    master_list = await session.execute(select(Master))
    keyboard_master = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for master in master_list:
        keyboard_master.add(KeyboardButton(master[0].name))
    return keyboard_master


async def delete_master_db(name: str):
    """
        Удаление мастера из БД
    :param name: str
    :return: bool (true в случае успеха)
    """
    session = session_maker()
    master = await session.execute(select(Master).where(Master.name == name))
    instance = master.scalars().first()
    if instance is None:
        return None
    await session.delete(instance)
    await session.commit()
    return True


async def get_admin_list() -> List:
    """
        Функция создает и возвращяет список администратов
    :return: List
    """
    session = session_maker()
    admin_list = await session.execute(select(Admin))
    result = []
    for admin in admin_list:
        result.append(admin[0].user_id)
    return result


async def delete_admin_db(user_id: int):
    """
        Удаление администратора из БД
    :param user_id: int (id телеграмм чата администратора)
    :return: bool (True в случае успеха)
    """
    session = session_maker()
    admin = await session.execute(select(Admin).where(Admin.user_id == user_id))
    instance = admin.scalars().first()
    if instance is None:
        return None
    await session.delete(instance)
    await session.commit()
    return True


async def get_admin_dict():
    """
        Создает и возвращяет словарь {id: name}
    :return: dict
    """
    session = session_maker()
    admin_list = await session.execute(select(Admin))
    result = {}
    for admin in admin_list:
        result[admin[0].user_id] = admin[0].username
    return result


async def get_admin_list_keyboard():
    """
        Создает и возвращяет клавиатуру с администраторами
    :return: ReplyKeyboardMarkup
    """
    admin_dict = await get_admin_dict()
    keyboard_admin_list = ReplyKeyboardMarkup(resize_keyboard=True)
    for key, value in admin_dict.items():
        keyboard_admin_list.insert(KeyboardButton(f"{value}-{key}"))
    return keyboard_admin_list


async def get_all_feedback():
    """
        Возвращяет текст всех отзывов
    :return: str
    """
    session = session_maker()
    qs = await session.execute(select(Feedback).order_by(Feedback.id))
    text = "\n".join([f"{item[0].master} - {item[0].feedback}" for item in qs])
    return text
