from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


def get_main_menu():
    keyboard = [
        [KeyboardButton(text="Проф"), KeyboardButton(text="Техподдержка")],
        [KeyboardButton(text="Отзывы"), KeyboardButton(text="нэкст")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
