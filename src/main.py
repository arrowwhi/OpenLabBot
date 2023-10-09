from sqlalchemy import create_engine

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import database
from helpers import make_row_keyboard
import registration
import start_router


# # Подключение базы данных
# engine = create_engine('postgresql://postgres:@localhost/open_lab')
# # Создание таблиц
# database.Base.metadata.create_all(engine)



async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token="6492618024:AAGfSiD4qpHcR7ddJHObAo3IjOGktKvjZUk")
    # Диспетчер
    dp = Dispatcher()

    # Регистрируем обработчики
    dp.include_router(start_router.start_router)
    dp.include_router(registration.reg_router)
    # потом убрать
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
