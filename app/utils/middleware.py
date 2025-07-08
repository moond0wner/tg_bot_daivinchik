"""
Модуль для необходимых middleware.
"""

import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


from ..database.requests import set_user


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

#caches = {"default": TTLCache(maxsize=10_000, ttl=0.1)}


class UserMiddleware(BaseMiddleware):
    """
    Проверяет находиться ли пользователь в базе данных, если нет то добавляет
    """
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        await set_user(tg_id=event.from_user.id, username=event.from_user.username)

        return await handler(event, data)

