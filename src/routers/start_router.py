import asyncio

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
# from aiogram.utils.keyboard import InlineKeyboardBuilder

# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.fsm.context import FSMContext

from src.helpers.helpers import make_row_keyboard, AdminFilter
from src.database.database import db, config
from src.routers import victorine
from src.helpers import texts

numbers_str = config.get('Telegram', 'admin_id')
admins = [int(num) for num in numbers_str.split(',')]

start_router = Router()


class AdminCommands(StatesGroup):
    reset = State()  # Ожидание имени
    check = State()


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
    await message.answer(texts.start_message)
    await asyncio.sleep(1)
    if message.from_user.id in db.all_users:
        await message.answer('Привет! Вижу, что ты уже зарегистрирован. Давай продолжим викторину!',
                             reply_markup=make_row_keyboard(['Начать викторину!']))
    else:
        await message.answer("Для начала давай зарегистрируемся.",
                             reply_markup=make_row_keyboard(['Регистрация']))


@start_router.message(Command('reset'))
async def reset(message: types.Message, state: FSMContext):
    """
    Обработчик команды /reset
    """
    if message.from_user.id not in admins:
        return
    await message.answer('Напишите id пользователя, которого хотите сбросить',
                         reply_markup=make_row_keyboard(['Свой', 'Отменить']))
    await state.set_state(AdminCommands.reset)


@start_router.message(Command('check'))
async def check_start(message: types.Message, state: FSMContext):
    if message.from_user.id not in admins:
        return
    await message.answer('Напишите id пользователя, которого хотите проверить',
                         reply_markup=make_row_keyboard(['Отменить']))
    await state.set_state(AdminCommands.check)


@start_router.message(AdminCommands.check)
async def check_user(message: types.Message, state: FSMContext):
    if message.from_user.id not in admins:
        await state.clear()
        return
    if message.text == 'Отменить':
        await message.answer('Отменено', reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return
    try:
        user_id = int(message.text)
    except ValueError:
        await message.answer('Неверный id', reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return
    user_info = await db.get_user_result(user_id)
    if user_info is None:
        await message.answer('Пользователь не найден', reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return
    if not user_info['is_completed']:
        await message.answer('Пользователь не закончил викторину')
    final_score = user_info['final_score']
    await message.answer(f'Результат пользователя {user_id}:\n'
                         f'Правильных ответов: {final_score}\n',reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


@start_router.message(AdminCommands.reset)
async def reset_confirm(message: types.Message, state: FSMContext):
    if message.from_user.id not in admins:
        await state.clear()
        return
    if message.text == 'Отменить':
        await message.answer('Отменено')
        await state.clear()
        return
    if message.text == 'Свой':
        if message.from_user.id not in db.all_users:
            await message.answer('Вы не зарегистрированы')
            await state.clear()
            return
        await db.reset_user(message.from_user.id)
        db.all_users.remove(message.from_user.id)
        del victorine.users_params[message.from_user.id]
        await message.answer('Сброшено')
        await state.clear()
        return
    try:
        user_id = int(message.text)
    except ValueError:
        await message.answer('Неверный id', reply_markup=make_row_keyboard([]))
        await state.clear()
        return
    if user_id not in db.all_users:
        await message.answer(f'{user_id} зарегистрирован')
        await state.clear()
        return
    await db.reset_user(user_id)
    db.all_users.remove(user_id)
    # victorine.users_params.pop(user_id)
    await message.answer('Сброшено')
    await state.clear()
    return
