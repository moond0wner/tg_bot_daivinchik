"""
Модуль с callback-обработчиком для возвращения в главное меню.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.utils.keyboards import get_inline_buttons

router = Router()

@router.callback_query(F.data == "back")
async def show_main_menu(callback: CallbackQuery) -> None:
    """Обрабатывает кнопку выхода в главное меню."""
    await callback.answer()
    await callback.message.answer(
        f"Привет, <b>{callback.from_user.full_name}!</b>",
        reply_markup=await get_inline_buttons(
            btns={
                "Моя анкета": "my_profile",
                "Смотреть анкеты": "get_profiles",
                "Сообщить о проблеме": "send_problem"
            }
        ),
        parse_mode='HTML'
    )
