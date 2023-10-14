from aiogram import Router, types
from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.fsm.context import FSMContext

from helpers import make_row_keyboard
from helpers import AdminFilter  # , admin_list

from database import db, config

numbers_str = config.get('Telegram', 'admin_id')
admins = [int(num) for num in numbers_str.split(',')]

start_router = Router()


@start_router.message(AdminFilter(admins=admins))
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
