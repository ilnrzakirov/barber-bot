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

from db.db import Admin
from settings import session_maker


class AdminState(StatesGroup):
    user_id = State()
    username = State()


async def add_admin(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username}")
    await AdminState.user_id.set()
    await message.answer("ID телеграма")


async def add_admin_user_id(message: types.Message, state: FSMContext):
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["user_id"] = message.text
    await AdminState.next()
    await message.answer("Теперь username")


async def add_admin_username(message: types.Message, state: FSMContext):
    logger.info(f"Получены данные {message.text} от {message.from_user.username}")
    async with state.proxy() as data:
        data["username"] = message.text
    admin = Admin(int(data["user_id"]), data["username"])
    session = session_maker()
    session.add(admin)
    await state.finish()
    await session.commit()
    await message.answer("Админ добавлен")


def register_handlers_owner(dispatcher: Dispatcher):
    dispatcher.register_message_handler(add_admin, commands=["add_admin"], state=None)
    dispatcher.register_message_handler(add_admin_user_id, state=AdminState.user_id)
    dispatcher.register_message_handler(add_admin_username, state=AdminState.username)
