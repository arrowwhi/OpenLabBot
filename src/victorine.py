from aiogram import Router, types
from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
# from aiogram.fsm.context import FSMContext

from helpers import make_inline_keyboard

from database import db


class VictorineState(StatesGroup):
    """
    Класс состояний для викторины
    """
    waiting_for_name = State()
    waiting_for_gender = State()


class Victorine:
    def __init__(self, tg_id):
        self.questions_count = None
        self.groups_count = None
        self.answers = None
        self.question = None
        self.user_id = tg_id
        self.current_group = None
        self.question_id = None
        self.group = None

    async def initialize(self):
        user = await db.get_user_current_question(self.user_id)
        print('\n\nuser:\n\n', user)
        if user:
            self.current_group = user.current_group
            self.question_id = user.current_question
        else:
            self.current_group = 1
            self.question_id = 1
            await db.add_user_current_question(self.user_id)
        self.groups_count = await db.get_groups_count()
        self.group = await db.get_group(self.current_group)
        self.questions_count = await db.count_questions_in_group(self.current_group)

    async def get_question_number(self):
        if self.question_id < self.questions_count:
            self.question_id += 1
        else:
            if self.current_group < self.groups_count:
                self.current_group += 1
                self.question_id = 1
                self.questions_count = await db.count_questions_in_group(self.current_group)
            else:
                print('Викторина закончена')
                db.update_user_current_question_complete(self.user_id)
                return None
        await db.update_user_current_question(self.user_id, self.question_id, self.current_group)
        await self.get_next_question()

    async def get_next_question(self):
        self.question = await db.get_question(self.current_group, self.question_id)
        print(self.question)
        self.answers = await db.get_answers(self.question['id'])

    def show_question(self):
        return self.question['question_text']
        # pass

    def show_answers_text(self):
        return [[answer['answer_text'], answer['id']] for answer in self.answers]

    def show_callback(self):
        return [answer['id'] for answer in self.answers]

    def get_choice(self, answer_id):
        for ans in self.answers:
            if ans['id'] == answer_id:
                return ans


users_params = {}

victorine_router = Router()


@victorine_router.message(lambda message: message.text == 'Начать викторину!' or Command('victorine'))
async def get_question(message: types.Message):
    user_id = message.from_user.id
    if users_params.get(user_id) is None:
        users_params[user_id] = Victorine(user_id)
        await users_params[user_id].initialize()
    await users_params[user_id].get_next_question()
    answer_texts = users_params[user_id].show_answers_text()
    users_params[user_id].answer_texts = answer_texts
    print(answer_texts)
    print(user_id)
    if users_params[user_id].current_group == 1:
        await message.answer(users_params[user_id].group.group_preview, reply_markup=types.ReplyKeyboardRemove())
    await message.answer(users_params[message.from_user.id].show_question(),
                         reply_markup=make_inline_keyboard(answer_texts))


@victorine_router.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    print(callback_query.data)
    user_id = callback_query.from_user.id
    print(user_id)
    print(callback_query.from_user.id)
    ans = users_params[user_id].get_choice(int(callback_query.data))
    print(ans)
    if ans:
        await callback_query.answer()
        reply = callback_query.message.text
        await db.add_user_answer(user_id, ans['question_id'], ans['id'], ans['is_correct'])
        reply += ('\n\nВы ответили:\n' + ans['answer_text'] + '\n\n')
        if ans['is_correct']:
            reply += 'Верно!\n\n'
        else:
            reply += 'Неверно:(\n\n'
        await callback_query.message.edit_text(reply, reply_markup=make_inline_keyboard([]))
        await callback_query.message.answer('Нажми "Далее", чтобы продолжить')
        await users_params[user_id].get_question_number()
        await callback_query.message.answer(users_params[user_id].show_question(),
                                            reply_markup=make_inline_keyboard(
                                                users_params[user_id].show_answers_text()))
    else:
        await callback_query.answer('Что-то пошло не так')
