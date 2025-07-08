"""
Модуль callback-обработчиков для реализации показа анкет.
"""
import logging

from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from app.database.requests import get_random_profile
from app.utils.config import settings
from app.utils.keyboards import get_inline_buttons
from app.handlers.callback.get_profile import get_profile, handler_my_profile
from app.database.requests import check_profile

router = Router()

@router.callback_query(F.data == "get_profiles")
async def handler_get_profile(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """Обрабатывает кнопку просмотра анкеты. Отправляет анкеты по одной пока они не закончатся."""
    await callback.answer()

    have_profile = await check_profile(callback.from_user.id)
    if have_profile:
        random_profile = await get_random_profile(callback.from_user.id)
        if random_profile:
            text = (f"{random_profile.name} - {random_profile.age}, {random_profile.city}\n"
                    f"{random_profile.description}")
            photo_path = f"{settings.FOLDER}/{random_profile.photo_id}.jpg"
            await bot.send_photo(
                chat_id=callback.from_user.id,
                photo=FSInputFile(photo_path),
                caption=text,
                reply_markup=await get_inline_buttons(
                    btns={
                        "❤": f"love_{random_profile.tg_id}",
                        "👎": "not_love",
                        "💤": "back"
                    }
                )
            )
        else:
            await callback.message.answer(
                "Извините, все профили закончились",
                reply_markup=await get_inline_buttons(
                    btns={
                        "💤": "back"
                    }
                )
            )
    else:
        await handler_my_profile(callback, state, bot)


@router.callback_query(F.data.startswith("love_"))
async def handler_love(callback: CallbackQuery, bot: Bot) -> None:
    """Обработка кнопки, когда пользователю понравилась чья-то анкета.
    После вызывает функцию для показа следующей анкеты."""
    await callback.answer()
    selected_profile = int(callback.data.split("_")[-1])
    owner_profile = await get_profile(callback.from_user.id)
    text = ("Твою анкету лайкнул пользователь:\n"
            f"{owner_profile.name} - {owner_profile.age}, {owner_profile.city}\n"
            f"{owner_profile.description}\n\n"
            f"Написать: @{callback.from_user.username}")
    try:
        await bot.send_photo(
            chat_id=selected_profile,
            caption=text,
            photo=FSInputFile(f"{settings.FOLDER}/{owner_profile.photo_id}.jpg"),
            reply_markup=await get_inline_buttons(
                btns={
                    "Смотреть дальше": "get_profiles",
                    "Главное меню": "back"
                }
            )
        )
    except Exception as e:
        await callback.message.answer("Произошла ошибка...")
        logging.error("Не удалось отправить пользователю (%d) сообщение, ошибка: %w", selected_profile, e)


@router.callback_query(F.data == "not_love")
async def handler_not_love(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """Если пользователю анкета не понравилась, бот просто пропускаёт и показывает дальше."""
    await callback.answer()
    await handler_get_profile(callback, state, bot)
