from aiogram import Router, F, types
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from helpers import make_row_keyboard
from database import db


class Registration(StatesGroup):
    """
    Класс состояний для регистрации
    """
    waiting_for_name = State()
    waiting_for_gender = State()
    waiting_for_age = State()
    waiting_for_education = State()
    waiting_for_edu_sector = State()
    waiting_for_confirm = State()


reg_router = Router()


@reg_router.message(F.text.lower() == 'регистрация')
async def start_registration(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, введи свои имя и фамилию.', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Registration.waiting_for_name)


@reg_router.message(Registration.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    if user_data.get('finished', False):
        await process_edu_sector(message, state)
        return
    await message.answer('Отлично! Теперь выбери свой пол.',
                         reply_markup=make_row_keyboard(['Мужской', 'Женский', 'Другой']))
    await state.set_state(Registration.waiting_for_gender)


@reg_router.message(Registration.waiting_for_gender)
async def process_gender(message: types.Message, state: FSMContext):
    if message.text not in ['Мужской', 'Женский', 'Другой']:
        await message.answer('Пожалуйста, выбери один из предложенных вариантов.')
        return
    await state.update_data(gender=message.text)
    user_data = await state.get_data()
    if user_data.get('finished', False):
        await process_edu_sector(message, state)
        return
    await message.answer('Отлично! Теперь введи свой возраст.', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Registration.waiting_for_age)


education_level = ['Неоконченное среднее',
                   'Среднее',
                   'Неоконченное высшее',
                   'Высшее',
                   'Ученая степень']


@reg_router.message(Registration.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Пожалуйста, введи возраст цифрами.')
        return
    await state.update_data(age=int(message.text))
    user_data = await state.get_data()
    if user_data.get('finished', False):
        await process_edu_sector(message, state)
        return
    await message.answer('Отлично! Теперь выбери свой уровень образования.',
                         reply_markup=make_row_keyboard(education_level))
    await state.set_state(Registration.waiting_for_education)


@reg_router.message(Registration.waiting_for_education)
async def process_education(message: types.Message, state: FSMContext):
    if message.text not in education_level:
        await message.answer('Пожалуйста, выбери один из предложенных вариантов.')
        return
    await state.update_data(education=message.text)
    if message.text == 'Неоконченное среднее' or message.text == 'Среднее':
        await process_edu_sector(message, state)
        return
    user_data = await state.get_data()
    if user_data.get('finished', False):
        await process_edu_sector(message, state)
        return
    await message.answer('Отлично! Теперь введи свою образовательную сферу.', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Registration.waiting_for_edu_sector)


@reg_router.message(Registration.waiting_for_edu_sector)
async def process_edu_sector(message: types.Message, state: FSMContext):
    await state.update_data(edu_sector=message.text)
    await state.update_data(finished=True)
    user_data = await state.get_data()
    ans = 'Проверь, правильно ли ты ввел свои данные:\n' \
          f'Имя: {user_data["name"]}\n' \
          f'Пол: {user_data["gender"]}\n' \
          f'Возраст: {user_data["age"]} лет\n' \
          f'Образование: {user_data["education"]}\n'
    if user_data.get('edu_sector', False):
        ans += f'Образовательная сфера: {user_data["edu_sector"]}'
    await message.answer(ans)
    await message.answer('Если всё верно, нажми "Подтвердить". Если нет - выбери то, что нужно изменить',
                         reply_markup=make_row_keyboard(['Редактировать имя',
                                                         'Редактировать пол',
                                                         'Редактировать возраст',
                                                         'Редактировать образование',
                                                         'Редактировать образовательную сферу',
                                                         'Подтвердить']))
    await state.set_state(Registration.waiting_for_confirm)


@reg_router.message(Registration.waiting_for_confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text == 'Подтвердить':
        # db.add_user(**await state.get_data())
        user_data = await state.get_data()
        await db.add_user(
            tg_id=message.from_user.id,
            name=user_data['name'],
            age=user_data['age'],
            gender=user_data['gender'],
            education=user_data['education'],
            edu_sector=user_data.get('edu_sector', None)
        )
        await message.answer('Спасибо за регистрацию!', reply_markup=make_row_keyboard(['Начать викторину!']))
        await state.clear()
    elif message.text == 'Редактировать имя':
        await state.set_state(Registration.waiting_for_name)
        await message.answer('Пожалуйста, введи свое имя и фамилию.')
    elif message.text == 'Редактировать пол':
        await state.set_state(Registration.waiting_for_gender)
        await message.answer('Выбери свой пол.',
                             reply_markup=make_row_keyboard(['Мужской', 'Женский', 'Другой']))
    elif message.text == 'Редактировать возраст':
        await state.set_state(Registration.waiting_for_age)
        await message.answer('Введи свой возраст.')
    elif message.text == 'Редактировать образование':
        await state.set_state(Registration.waiting_for_education)
        await message.answer('Выбери свой уровень образования.',
                             reply_markup=make_row_keyboard(education_level))
    elif message.text == 'Редактировать образовательную сферу':
        await state.set_state(Registration.waiting_for_edu_sector)
        await message.answer('Введи свою образовательную сферу.')
    else:
        await message.answer('Пожалуйста, выбери один из предложенных вариантов.')
        return
