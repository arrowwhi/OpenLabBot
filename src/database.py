from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base


# Создание базового класса для определения моделей
Base = declarative_base()


# Определение моделей для таблиц


# Класс для записи уровней образования
class Edu(Base):
    __tablename__ = 'edus'

    id = Column(Integer, primary_key=True)
    name = Column(String)


# класс для записи пользователей
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=True)
    education = Column(Integer, ForeignKey('edus.id'), nullable=False)
    edu_sector = Column(String, nullable=True)


# класс для записи групп вопросов
class QuestionGroup(Base):
    __tablename__ = 'question_groups'

    id = Column(Integer, primary_key=True)
    group_name = Column(String, nullable=False)
    group_preview = Column(String)


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
    is_correct = Column(Boolean)


# класс для записи ответов пользователей
class UserAnswer(Base):
    __tablename__ = 'users_answers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    answer_id = Column(Integer, ForeignKey('answers.id'))
    is_correct = Column(Boolean)
