import asyncio
from datetime import datetime
from sqlalchemy import func, BigInteger, and_

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
# from sqlalchemy.orm import sessionmaker, selectinload
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
import configparser


# Создание базового класса для определения моделей
Base = declarative_base()


#       Определение моделей для таблиц


# класс для записи групп вопросов
class QuestionGroup(Base):
    __tablename__ = 'question_groups'

    id = Column(Integer, primary_key=True)
    group_name = Column(String, nullable=False)
    group_preview = Column(String)


# класс для записи пользователей
class User(Base):
    __tablename__ = 'users'

    # id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=True)
    education = Column(String, nullable=False)
    edu_sector = Column(String, nullable=True)
    create_date = Column(DateTime, default=datetime.utcnow)


# класс для записи вопросов
class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    in_group_id = Column(Integer)
    question = Column(String)
    group_id = Column(Integer, ForeignKey('question_groups.id'))


# класс для записи ответов
class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    answer_text = Column(String)
    answer_description = Column(String)
    is_correct = Column(Boolean)


# класс для записи ответов пользователей
class UserAnswer(Base):
    __tablename__ = 'users_answers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.tg_id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    answer_id = Column(Integer, ForeignKey('answers.id'))
    is_correct = Column(Boolean)


# Класс для отслеживания текущего вопроса пользователя
class UserCurrentQuestion(Base):
    __tablename__ = 'user_current_question'

    tg_id = Column(BigInteger, primary_key=True)
    current_group = Column(Integer, ForeignKey('question_groups.id'), default=1)
    current_question = Column(Integer, default=1)
    is_completed = Column(Boolean, default=False)
    final_score = Column(Integer, default=0)

# Класс для работы с базой данных
class Database:
    def __init__(self, login, password, host, port, db_name):
        # Подключение базы данных
        database_url = f'postgresql+asyncpg://{login}:{password}@{host}:{port}/{db_name}'
        self.engine = create_async_engine(database_url, echo=True)

        # Создание фабрики сессий SQLAlchemy
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

        self.all_users = []

    # Создание таблиц в базе данных
    async def create_tables(self):
        print("ok")
        # Base.metadata.create_all(self.engine)
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # Получение списка всех пользователей
    async def get_all_users(self):
        async with self.session() as session:
            try:
                query = select(User.tg_id)
                result = await session.execute(query)
                users = result.scalars().all()
                return [user for user in users]
            except Exception as e:
                print(f"An error occurred while fetching all users: {e}")
                return []

    # Добавление нового пользователя в базу данных
    async def add_user(self, tg_id, name, age, gender, education, edu_sector):
        # Создаем объект User для вставки
        new_user = User(
            name=name,
            tg_id=tg_id,
            age=age,
            gender=gender,
            education=education,
            edu_sector=edu_sector,
            create_date=datetime.utcnow()
        )

        async with self.session() as session:
            session.add(new_user)
            await session.commit()
        self.all_users.append(tg_id)

    # Добавление ответа пользователя на вопрос в базу данных
    async def add_user_answer(self, user_id, question_id, answer_id, is_correct):
        new_answer = UserAnswer(
            user_id=user_id,
            question_id=question_id,
            answer_id=answer_id,
            is_correct=is_correct
        )

        async with self.session() as session:
            session.add(new_answer)
            await session.commit()

        # Получение вопроса по заданным параметрам
    async def get_question(self, question_group_id, question_id):
        async with (self.session() as session):
            try:
                query = select(Question) \
                    .filter(Question.group_id == question_group_id, Question.in_group_id == question_id)
                question = await session.execute(query)
                question = question.scalars().first()
                if question:
                    return {
                        'id': question.id,
                        'in_group_id': question.in_group_id,
                        'question_text': question.question.replace('n', "\n"),
                        'group_id': question.group_id
                    }
                else:
                    return None
            except Exception as e:
                # Handle any exceptions here
                print(f"An error occurred while fetching the question: {e}")
                return None

    # Получение ответов на вопрос из базы данных
    async def get_answers(self, question_id):
        async with (self.session() as session):
            try:
                query = select(Answer) \
                    .filter(Answer.question_id == question_id)
                answers = await session.execute(query)
                answers = answers.scalars().all()
                if answers:
                    return [{
                        'id': answer.id,
                        'question_id': answer.question_id,
                        'answer_text': answer.answer_text,
                        'is_correct': answer.is_correct
                    } for answer in answers]
                else:
                    return None
            except Exception as e:
                print(f"An error occurred while fetching the answers: {e}")
                return None

    # Получение количества групп вопросов
    async def get_groups_count(self):
        async with self.session() as session:
            try:
                query = select(func.count(QuestionGroup.id))
                result = await session.execute(query)
                count = result.scalar()
                return count
            except Exception as e:
                print(f"An error occurred while counting groups: {e}")
                return None

    # Подсчет количества вопросов в указанной группе
    async def count_questions_in_group(self, group_id):
        async with self.session() as session:
            try:
                query = select(func.count(Question.id)) \
                    .where(Question.group_id == group_id)
                result = await session.execute(query)
                count = result.scalar()
                return count
            except Exception as e:
                print(f"An error occurred while counting questions in the group: {e}")
                return None

    # Получение пользователя по Telegram ID
    async def get_user_by_tg_id(self, tg_id):
        async with self.session() as session:
            try:
                query = select(User) \
                    .filter(User.tg_id == tg_id)
                user = await session.execute(query)
                user = user.scalars().first()
                return user
            except Exception as e:
                print(f"An error occurred while fetching the user by tg_id: {e}")
                return None

    # Добавление информации о текущем вопросе пользователя
    async def add_user_current_question(self, tg_id):
        # Создаем объект UserCurrentQuestion для вставки
        new_user_current_question = UserCurrentQuestion(
            tg_id=tg_id,
            current_group=1,
            current_question=1
        )

        async with self.session() as session:
            session.add(new_user_current_question)
            await session.commit()

    # Получение информации о текущем вопросе пользователя
    async def get_user_current_question(self, tg_id):
        async with self.session() as session:
            try:
                query = select(UserCurrentQuestion) \
                    .filter(UserCurrentQuestion.tg_id == tg_id)
                user_current_question = await session.execute(query)
                user_current_question = user_current_question.scalars().first()
                return user_current_question
            except Exception as e:
                print(f"An error occurred while fetching user_current_question by tg_id: {e}")
                return None

    # Получение информации о группе вопросов
    async def get_group(self, group_id):
        async with self.session() as session:
            try:
                query = select(QuestionGroup) \
                    .filter(QuestionGroup.id == group_id)
                group = await session.execute(query)
                group = group.scalars().first()
                return group
            except Exception as e:
                print(f"An error occurred while fetching the group: {e}")
                return None

    # Обновление информации о текущем вопросе пользователя
    async def update_user_current_question(self, tg_id, question_id, group_id):
        async with self.session() as session:
            try:
                query = select(UserCurrentQuestion) \
                    .filter(UserCurrentQuestion.tg_id == tg_id)
                user_current_question = await session.execute(query)
                user_current_question = user_current_question.scalars().first()

                if user_current_question:
                    user_current_question.current_question = question_id
                    user_current_question.current_group = group_id

                    await session.commit()
                    return True
                else:
                    return False
            except Exception as e:
                print(f"An error occurred while updating user_current_question: {e}")
                return False

    # Обновление информации о завершении опроса пользователя
    async def update_user_current_question_complete(self, tg_id):
        async with self.session() as session:
            try:
                query = select(UserAnswer) \
                    .filter(and_(UserAnswer.user_id == tg_id, UserAnswer.is_correct))

                user_answers = await session.execute(query)
                user_answers = user_answers.scalars().all()

                total_score = sum(1 for _ in user_answers)

                query = select(UserCurrentQuestion) \
                    .filter(UserCurrentQuestion.tg_id == tg_id)
                user_current_question = await session.execute(query)
                user_current_question = user_current_question.scalars().first()

                if user_current_question:
                    user_current_question.is_completed = True
                    user_current_question.final_score = total_score

                    await session.commit()
                    return total_score
                else:
                    return False
            except Exception as e:
                print(f"An error occurred while updating UserCurrentQuestion: {e}")
                return False


config = configparser.ConfigParser()
config.read('config.ini')

# Получение значения из секции "Database"
host = config.get('Database', 'host')
port = config.get('Database', 'port')
username = config.get('Database', 'username')
password = config.get('Database', 'password')
database = config.get('Database', 'database')

db = Database(username, password, host, port, database)


async def main():
    q = await db.get_question(1, 1)
    print(q)


if __name__ == "__main__":
    asyncio.run(main())
