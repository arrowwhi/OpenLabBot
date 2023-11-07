from typing import Union, Optional

from aiogram import types
from aiogram.filters import BaseFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message  # , InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.database import db


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [[KeyboardButton(text=item)] for item in items]
    return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=False, one_time_keyboard=True)


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


# ['Редактировать имя',
# 'Редактировать пол',
# 'Редактировать возраст',
# 'Редактировать образование',
# 'Редактировать образовательную сферу',
# 'Подтвердить']

class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int] = None


def get_confirm_pi_keyboard(sf=False):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ Подтвердить", callback_data=NumbersCallbackFactory(action="confirm_pi")
    )
    builder.button(
        text="Редактировать имя", callback_data=NumbersCallbackFactory(action="change_pi", value=1)
    )
    builder.button(
        text="Редактировать пол", callback_data=NumbersCallbackFactory(action="change_pi", value=2)
    )
    builder.button(
        text="Редактировать возраст", callback_data=NumbersCallbackFactory(action="change_pi", value=3)
    )
    builder.button(
        text="Редактировать образование", callback_data=NumbersCallbackFactory(action="change_pi", value=4)
    )
    print("SF = ", sf)
    if sf:
        builder.button(
            text="Редактировать образовательную сферу",
            callback_data=NumbersCallbackFactory(action="change_pi", value=5)
        )
    builder.adjust(1)
    return builder.as_markup()


def get_confirm_answer_keyboard(flag=True, next_group=False):
    builder = InlineKeyboardBuilder()
    if flag:
        builder.button(
            text='Объяснение',
            callback_data='explanation'
        )
    if next_group:
        txt = 'Следующая группа'
    else:
        txt = 'Следующий вопрос'
    builder.button(
        text=txt,
        callback_data='next_question'
    )
    builder.adjust(2)
    return builder.as_markup()


def get_final_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Завершить викторину',
        callback_data='next_question'
    )
    builder.adjust(1)
    return builder.as_markup()


def get_resend_question():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Отправить вопрос ещё раз',
        callback_data='resend_question'
    )
    builder.adjust(1)
    return builder.as_markup()


def get_next_question_button():
    row = KeyboardButton(text='Следующий вопрос')
    return ReplyKeyboardMarkup(keyboard=[[row]], resize_keyboard=False, one_time_keyboard=True)
