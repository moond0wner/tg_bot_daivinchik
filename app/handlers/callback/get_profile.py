"""
Модуль с callback-обработчикам для отправки профиля пользователю.
"""

import asyncio
import logging

from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from app.database.requests import check_profile, get_profile
from app.handlers.states import Profile
from app.utils.config import settings

router = Router()

@router.callback_query(F.data == "my_profile")
async def handler_my_profile(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """Обрабатывает кнопку просмотра анкеты пользователя.
    Если его анкета есть - отправляет пользователю.
    Если его анкеты нет - начинает процесс её создания."""
    await callback.answer()

    if not await check_profile(callback.from_user.id):
        await callback.message.answer("Для поиска знакомств давайте создадим анкету...")
        await asyncio.sleep(1)
        await callback.message.answer("Как мне тебя называть?")
        await state.set_state(Profile.name)
    else:
        profile = await get_profile(callback.from_user.id)
        result_text = (f"{profile.name} - {profile.age}, {profile.city}\n"
                       f"{profile.description}")
        try:
            await callback.message.answer("Ваша анкета:")
            photo_path = f"{settings.FOLDER}/{profile.photo_id}.jpg"
            print(f"Photo path: {photo_path}")
            await bot.send_photo(chat_id=callback.from_user.id,
                                 photo=FSInputFile(photo_path),
                                 caption=result_text
                                 )
        except Exception as e:
            await callback.message.answer("Произошла ошибка...")
            logging.error("Ошибка в ходе отправки информации о профиле пользователя: ", str(e))