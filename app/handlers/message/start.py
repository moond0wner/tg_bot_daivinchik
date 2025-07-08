"""
Модуль с message-обработчиком для старта бота пользователем.
"""

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.utils.keyboards import get_inline_buttons

router = Router()

@router.message(CommandStart())
async def show_main_menu(message: Message) -> None:
    await message.answer(
        f"Привет, <b>{message.from_user.full_name}!</b>",
        reply_markup=await get_inline_buttons(
            btns={
                "Моя анкета": "my_profile",
                "Смотреть анкеты": "get_profiles",
                "Сообщить о проблеме": "send_problem"
            }
        ),
        parse_mode='HTML'
    )
