from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from helpers import make_row_keyboard

start_router = Router()


@start_router.message(Command('start'))
async def start(message: types.Message):
    """
    Обработчик команды /start
    """
    await message.answer('привет! Для начала нужно зарегистрироваться.',
                         reply_markup=make_row_keyboard(['Регистрация']))
