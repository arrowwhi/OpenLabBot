import asyncio

from aiogram import Router, F, types
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.helpers.helpers import make_row_keyboard, get_confirm_pi_keyboard, NumbersCallbackFactory
from src.database.database import db


# Определение класса StatesGroup для управления состояниями регистрации пользователя.
class Registration(StatesGroup):
    waiting_for_name = State()  # Ожидание имени
    waiting_for_gender = State()  # Ожидание пола
    waiting_for_age = State()  # Ожидание возраста
    waiting_for_education = State()  # Ожидание уровня образования
    waiting_for_edu_sector = State()  # Ожидание образовательной сферы
    waiting_for_confirm = State()  # Ожидание подтверждения


# Создание экземпляра роутера для управления регистрацией пользователей.
reg_router = Router()


# Обработчик для начала процесса регистрации при отправке сообщения "регистрация".
@reg_router.message(F.text.lower() == 'регистрация')
async def start_registration(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, введи свои имя и фамилию.', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Registration.waiting_for_name)


# Обработчики для каждого этапа процесса регистрации:
# - process_name: Получение имени пользователя и переход к следующему этапу.
# - process_gender: Получение пола пользователя и переход к следующему этапу.
# - process_age: Получение возраста пользователя и переход к следующему этапу.
# - process_education: Получение уровня образования пользователя и переход к следующему этапу.
# - process_edu_sector: Получение образовательной сферы и завершение регистрации.
# - process_confirm: Подтверждение регистрации или предложение отредактировать данные.
# Все эти обработчики промежуточно сохраняют данные в контексте состояния FSMContext.
# В конце успешной регистрации данные отправляются в базу данных.
# В случае запроса на редактирование, происходит переход к соответствующему этапу регистрации.

@reg_router.message(Registration.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    if user_data.get('finished', False):
        await process_edu_sector(message, state)
        return
    await message.answer('Супер! Теперь выбери свой пол.',
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


# Определение уровней образования в виде списка.
education_level = ['Неоконченное среднее',
                   'Среднее',
                   'Неоконченное высшее',
                   'Высшее',
                   'Ученая степень']


@reg_router.message(Registration.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Пожалуйста, введите возраст цифрами.')
        return
    print(message.text)
    if int(message.text) < 4 or int(message.text) > 100:
        await message.answer('Пожалуйста, введите реальный возраст.')
        return
    await state.update_data(age=int(message.text))
    user_data = await state.get_data()
    if user_data.get('finished', False):
        await process_edu_sector(message, state)
        return
    await message.answer('Потрясающе! Теперь выбери свой уровень образования.',
                         reply_markup=make_row_keyboard(education_level))
    await state.set_state(Registration.waiting_for_education)


@reg_router.message(Registration.waiting_for_education)
async def process_education(message: types.Message, state: FSMContext):
    if message.text not in education_level:
        await message.answer('Пожалуйста, выбери один из предложенных вариантов.')
        return
    await state.update_data(education=message.text)
    if message.text == 'Неоконченное среднее' or message.text == 'Среднее':
        await state.update_data(edu_sphere=False)
        await state.set_state(Registration.waiting_for_confirm)
        await process_edu_sector(message, state)
        return
    await state.update_data(edu_sphere=True)
    user_data = await state.get_data()
    if user_data.get('finished', False):
        await process_edu_sector(message, state)
        return
    await message.answer('Последнее - веди свою сферу образования.', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Registration.waiting_for_edu_sector)


@reg_router.message(Registration.waiting_for_edu_sector)
async def process_edu_sector(message: types.Message, state: FSMContext):
    await state.update_data(edu_sector=message.text)
    await state.update_data(finished=True)
    sf = False
    user_data = await state.get_data()
    ans = 'Проверь, правильно ли ты ввел свои данные:\n\n' \
          f'Имя: {user_data["name"]}\n' \
          f'Пол: {user_data["gender"]}\n' \
          f'Возраст: {user_data["age"]} лет\n' \
          f'Образование: {user_data["education"]}\n'
    if user_data.get('edu_sphere', False):
        print(user_data.get('edu_sector', False))
        ans += f'Образовательная сфера: {user_data["edu_sector"]}'
        sf = True
    await message.answer(ans + '\n\n'+'Если всё верно, нажми "Подтвердить". Если нет - выбери то, что нужно изменить',
                         reply_markup=get_confirm_pi_keyboard(sf))
    await state.set_state(Registration.waiting_for_confirm)


@reg_router.callback_query(NumbersCallbackFactory.filter())
async def process_confirm(callback: types.CallbackQuery,
                          callback_data: NumbersCallbackFactory, state: FSMContext):
    if callback_data.action == 'confirm_pi':
        user_data = await state.get_data()
        task = asyncio.create_task(db.add_user(
            tg_id=callback.from_user.id,
            name=user_data['name'],
            age=user_data['age'],
            gender=user_data['gender'],
            education=user_data['education'],
            edu_sector=user_data.get('edu_sector', None)
        ))
        text = callback.message.text.split('\n\n')[1]

        await callback.message.edit_text("Ваши данные:\n\n" + text)
        # await callback.message.edit_reply_markup()
        await callback.answer('Успешно!')
        await callback.message.answer('Давай начнем!', reply_markup=make_row_keyboard(['Начать викторину!']))
        await state.clear()
    elif callback_data.action == 'change_pi':
        await callback.answer()
        await callback.message.edit_text(callback.message.text.split('\n\n')[1])
        if callback_data.value == 1:
            await state.set_state(Registration.waiting_for_name)
            await callback.message.answer('Пожалуйста, введи свое имя и фамилию.')
        elif callback_data.value == 2:
            await state.set_state(Registration.waiting_for_gender)
            await callback.message.answer('Выбери свой пол.',
                                          reply_markup=make_row_keyboard(['Мужской', 'Женский', 'Другой']))
        elif callback_data.value == 3:
            await state.set_state(Registration.waiting_for_age)
            await callback.message.answer('Введи свой возраст.')
        elif callback_data.value == 4:
            await state.set_state(Registration.waiting_for_education)
            await callback.message.answer('Выбери свой уровень образования.',
                                          reply_markup=make_row_keyboard(education_level))
        elif callback_data.value == 5:
            await state.set_state(Registration.waiting_for_edu_sector)
            await callback.message.answer('Введи свою образовательную сферу.')
        else:
            await callback.answer('Ой, вы попали не туда...')
    else:
        await callback.answer('Ой, вы попали не туда...')
        return
