"""
Модуль с callback-обработчиком для отправки репорта разработчику.
"""

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.handlers.states import Problem

router = Router()

@router.callback_query(F.data == "send_problem")
async def handler_send_problem(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработка кнопки отправки сообщения разработчику."""
    await callback.answer()
    await callback.message.answer("Здравствуйте, опишите свою проблему одним сообщением.")
    await state.set_state(Problem.text_problem)

