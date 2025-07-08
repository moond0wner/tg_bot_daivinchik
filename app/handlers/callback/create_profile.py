"""
Модуль callback обработчиков для создания профиля.
"""

import logging

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.handlers.callback.get_profile import handler_my_profile
from app.handlers.callback.scroll_profiles import handler_get_profile
from app.handlers.states import Profile
from app.database.requests import create_profile

router = Router()

@router.callback_query(Profile.gender, F.data == "male")
async def get_gender(callback: CallbackQuery, state: FSMContext) -> None:
    """Принимает сообщение о мужском поле, сохраняет и устанавливает состояние получения города."""
    await state.update_data(gender="male")
    await state.set_state(Profile.city)
    await callback.answer()
    await callback.message.answer("В каком городе ты проживаешь?")


@router.callback_query(F.data == "female")
async def get_gender(callback: CallbackQuery, state: FSMContext) -> None:
    """Принимает сообщение о женском поле, сохраняет и устанавливает состояние получения города."""
    await state.update_data(gender="female")
    await state.set_state(Profile.city)
    await callback.answer()
    await callback.message.answer("В каком городе ты проживаешь?")


@router.callback_query(F.data == "profile_complete")
async def new_profile(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """Обрабатывает удовлетворенность пользователя созданной анкеты и вызывает функцию для записи анкеты в БД."""
    await callback.answer()

    data = await state.get_data()

    tg_id = callback.from_user.id
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    city = data.get("city")
    description = data.get("description")
    photo_id = data.get("photo_id")

    try:
        await create_profile(tg_id, name, age, gender, city, description, photo_id)
        await callback.message.answer("Заявка успешно создана!")
        await handler_get_profile(callback, state, bot)
    except Exception as e:
        await callback.message.answer("Произошла ошибка...")
        logging.error("Ошибка при вызове create_profile: ", str(e))



@router.callback_query(F.data == "recreate_profile")
async def recreate_profile(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """Обрабатывает неудовлетворенность пользователя созданной анкеты и вызывает функцию для повторного создания."""
    await state.clear()
    await handler_my_profile(callback, state, bot)

