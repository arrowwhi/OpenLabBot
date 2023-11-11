
import asyncio

import logging
from aiogram import Bot, Dispatcher

from src.database.database import db, config
from src.routers import victorine, registration, start_router


async def main():
    token = config.get('Telegram', 'token')
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token=token)
    # Диспетчер
    dp = Dispatcher()

    # await db.create_tables()
    db.all_users = await db.get_all_users()

    # Регистрируем обработчики
    dp.include_router(start_router.start_router)
    dp.include_router(registration.reg_router)
    dp.include_router(victorine.victorine_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
