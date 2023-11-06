import asyncio

from aiogram import Router, types
from src.helpers.helpers import make_row_keyboard, get_confirm_answer_keyboard
from src.database.database import db


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
        self.finished = False
        self.total_score = 0
        self.message = None
        self.is_answered = False
        self.question_description = ''

    async def initialize(self):
        user = await db.get_user_current_question(self.user_id)
        if user:
            self.current_group = user.current_group
            self.question_id = user.current_question
            self.finished = user.is_completed
            self.total_score = user.final_score
        else:
            self.current_group = 1
            self.question_id = 1
            await db.add_user_current_question(self.user_id)
        self.groups_count = await db.get_groups_count()
        self.group = await db.get_group(self.current_group)
        self.questions_count = await db.count_questions_in_group(self.current_group)

    async def get_question_number(self):
        self.is_answered = False

        if self.question_id < self.questions_count:
            self.question_id += 1
        else:
            if self.current_group < self.groups_count:
                self.current_group += 1
                self.question_id = 1
                self.questions_count = await db.count_questions_in_group(self.current_group)
            else:
                print('Викторина закончена')
                self.total_score = await db.update_user_current_question_complete(self.user_id)
                self.finished = True
                return None

        await db.update_user_current_question(self.user_id, self.question_id, self.current_group)
        await self.get_next_question()

    async def get_next_question(self):
        print(self.current_group, self.question_id)
        self.question = await db.get_question(self.current_group, self.question_id)
        print(self.question)
        self.answers = await db.get_answers(self.question['id'])

    def show_question(self):
        return self.question['question_text']
        # pass

    def show_answers_text_id_with_callback(self):
        return [[answer['answer_text'], answer['id']] for answer in self.answers]

    def show_answers_text(self):
        return [answer['answer_text'] for answer in self.answers]

    def get_right_answer_number(self):
        for i in range(len(self.answers)):
            if self.answers[i]['is_correct']:
                return i

    def show_callback(self):
        return [answer['id'] for answer in self.answers]

    def get_choice(self, answer_id):
        for ans in self.answers:
            if ans['id'] == answer_id:
                return ans

    def get_choice_by_number(self, number):
        return self.answers[number]


victorine_router = Router()

users_params = {}


@victorine_router.message(lambda message: message.text == 'Начать викторину!')
async def get_question(message: types.Message):
    user_id = message.from_user.id

    if users_params.get(user_id) is None:
        users_params[user_id] = Victorine(user_id)
        await users_params[user_id].initialize()

    if users_params[user_id].finished:
        await message.answer('Викторина закончена!',
                             reply_markup=make_row_keyboard(['Показать результаты']))
        return

    users_params[user_id].message = message
    await users_params[user_id].get_next_question()
    answer_texts = users_params[user_id].show_answers_text_id_with_callback()
    users_params[user_id].answer_texts = answer_texts
    print(answer_texts)
    print(user_id)
    if users_params[user_id].question_id == 1:
        await message.answer(users_params[user_id].group.group_preview)
    await send_next_question_message(message)


@victorine_router.callback_query()
async def process_callback(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(callback.message.text)
    if callback.data == 'resend_question':
        await callback.message.delete()
        await send_next_question_message(user_id=callback.from_user.id)
    if callback.data == 'explanation':
        q_id = users_params[callback.from_user.id].question_id == users_params[callback.from_user.id].questions_count
        await callback.message.answer(users_params[callback.from_user.id].question_description,
                                      reply_markup=get_confirm_answer_keyboard(False, q_id))
        return
    elif callback.data == 'next_question':
        # await users_params[callback.from_user.id].get_question_number()
        if users_params[callback.from_user.id].finished:
            await callback.message.answer('Викторина закончена!',
                                          reply_markup=make_row_keyboard(['Показать результаты']))
            return
        await send_next_question_message(user_id=callback.from_user.id)
        return


@victorine_router.poll_answer()
async def poll_answer(poll_ans: types.PollAnswer):
    # this handler starts after user chose any answer
    print(poll_ans)
    user_id = poll_ans.user.id
    users_params[user_id].is_answered = True
    ans_id = users_params[user_id].show_answers_text_id_with_callback()[poll_ans.option_ids[0]][1]
    print(ans_id)
    ans = users_params[user_id].get_choice(ans_id)
    print(ans)
    users_params[user_id].question_description = users_params[user_id].question['answer_description']
    if ans['is_correct']:
        reply = 'Верно!'
    else:
        reply = 'Неверно:(\n'
        reply += 'Правильный ответ: ' + users_params[user_id].get_choice_by_number(
            users_params[user_id].get_right_answer_number())['answer_text']
    q_id = users_params[user_id].question_id == users_params[user_id].questions_count
    await users_params[user_id].message.answer(reply, reply_markup=get_confirm_answer_keyboard(True, q_id))
    try:
        await db.add_user_answer(user_id, ans['question_id'], ans_id, ans['is_correct'])
    except Exception as e:
        print(e)
    try:
        await users_params[user_id].get_question_number()
    except Exception as e:
        print(e)


@victorine_router.message(lambda message: message.text == 'Показать результаты')
async def show_results(message: types.Message):
    user_id = message.from_user.id
    if users_params.get(user_id) is None:
        await message.answer('Вы ещё не начали викторину!')
        return
    if users_params[user_id].finished:
        await message.answer('Викторина закончена!')
        await message.answer(f'Ваш результат: {users_params[user_id].total_score} баллов')
        return
    await message.answer('Вы ещё не закончили викторину!')
    return


async def send_next_question_message(message: types.Message = None, user_id=None):
    if not user_id:
        user_id = message.from_user.id
    if not message:
        message = users_params[user_id].message
    if users_params[user_id].question_id == users_params[user_id].questions_count:
        await message.answer(users_params[user_id].group.group_preview)
        await asyncio.sleep(1)
    await message.answer_poll(question=users_params[user_id].show_question(),
                              options=users_params[user_id].show_answers_text(),
                              type='quiz',
                              correct_option_id=users_params[user_id].get_right_answer_number(),
                              is_anonymous=False)
