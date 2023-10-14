from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from helpers import make_row_keyboard
from helpers import AdminFilter, admin_list

from database import db

start_router = Router()


@start_router.message(AdminFilter(admins=[918616493]))
async def start(message: types.Message):
    """
    Блокер
    """
    await message.answer('YOU SHALL NOT PASS!')


@start_router.message(Command('start'))
async def start(message: types.Message):
    """
    Обработчик команды /start
    """
    if message.from_user.id in db.all_users:
        await message.answer('Привет! Вижу, что ты уже зарегистрирован. Давай продолжим викторину!',
                             reply_markup=make_row_keyboard(['Начать викторину!']))
    else:
        await message.answer('Привет! Для начала нужно зарегистрироваться.',
                         reply_markup=make_row_keyboard(['Регистрация']))



