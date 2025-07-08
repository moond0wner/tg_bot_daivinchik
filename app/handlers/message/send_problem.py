"""
Модуль с message-обработчиком для отправки баг-репорта разработчику.
"""
import logging

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.handlers.states import Problem
from app.utils.config import settings


router = Router()

@router.message(Problem.text_problem)
async def send_problem(message: Message, state: FSMContext, bot: Bot) -> None:
    """Обработка сообщения от пользователя для отправки разработчику."""
    text = (f"Вам отправлено сообщение от пользователя {message.from_user.full_name} (@{message.from_user.username}, {message.from_user.id}):\n\n"
            f'"{message.text}"')
    try:
        await bot.send_message(chat_id=settings.DEVELOPER_ID, text=text)
        await message.answer("Сообщение успешно отправлено разработчику.")
    except Exception as e:
        logging.error("Ошибка отправки сообщения разработчику: %w", e)
        await message.answer("Произошла ошибка...")
    await state.clear()