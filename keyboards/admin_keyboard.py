from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

button_open_day = KeyboardButton("/open_day")
button_add_master = KeyboardButton("/add_master")

keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_admin.add(button_open_day).add(button_add_master)
