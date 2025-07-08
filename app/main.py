"""
Модуль для запуска телеграм-бота.
"""

import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app.database.engine import start_db
from app.database.engine import redis
from app.handlers import router
from app.utils.middleware import UserMiddleware
from app.utils.config import settings


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def main() -> None: 
    """Запуск бота"""
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=RedisStorage(redis=redis))
    
    dp.include_router(router)
    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await start_db()
        await dp.start_polling(bot)
    except ValueError as e:
        logging.error("ValueError occurred: %s: ", e)
    except KeyError as e:
        logging.error("KeyError occurred: %s:", e)
    finally:
        await bot.session.close()
        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот выключен.")