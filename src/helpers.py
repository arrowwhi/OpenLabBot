# from abc import ABC
from typing import Union

from aiogram import types
from aiogram.filters import BaseFilter
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message  # , InlineKeyboardMarkup, InlineKeyboardButton

from database import db

admin_list = [918616493]


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=False, one_time_keyboard=True)


def make_inline_keyboard(buttons):
    """
    Генерирует инлайн-клавиатуру на основе переданных кнопок.
    :param buttons: Список кнопок в формате [("текст кнопки", "callback_data")]
    :return: Объект InlineKeyboardMarkup
    """
    keyboard_buttons = []  # Создаем пустой список для кнопок

    for button_text, callback_data in buttons:
        button = types.InlineKeyboardButton(text=button_text, callback_data=str(callback_data))
        keyboard_buttons.append(button)  # Добавляем кнопку в список кнопок

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[keyboard_buttons])
    return keyboard


class AdminFilter(BaseFilter):
    def __init__(self, admins: Union[str, list]):
        self.admin_list = admins

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.admin_list, str):
            return not message.from_user.id != self.admin_list
        else:
            return message.from_user.id not in self.admin_list


class VictorineFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        user = await db.get_user_by_tg_id(message.from_user.id)
        if user and message.text == 'Начать викторину!':
            return True
        return False
