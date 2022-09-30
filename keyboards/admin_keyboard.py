from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

button_get_our_hair_cut = KeyboardButton("/Записатся")
button_location = KeyboardButton("/Месторасположение")

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_client.add(button_get_our_hair_cut).add(button_location)
