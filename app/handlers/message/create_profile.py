"""
Модуль message обработчиков для создания профиля.
"""
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

import app.utils.validation as vld
from app.utils.keyboards import get_inline_buttons
from app.handlers.states import Profile
from app.utils.config import settings

router = Router()

@router.message(Profile.name, F.text)
async def get_name(message: Message, state: FSMContext) -> None:
    """Принимает имя пользователя, валидирует. Если валидация успешна, то вызывает состояние для приёма возраста."""
    try:
        name = vld.UserName(name=message.text)
        await state.update_data(name=name.name)
        await state.set_state(Profile.age)
        await message.answer(f"Хорошо {name.name}, сколько тебе лет?")
    except ValueError as e:
        await message.answer(f"Ошибка, неверное имя: {e}")


@router.message(Profile.age, F.text)
async def get_age(message: Message, state: FSMContext) -> None:
    """Принимает возраст пользователя, валидирует, вызывает состояние выбора пола."""
    try:
        age = vld.UserAge(age=message.text)
        await state.update_data(age=age.age)
        await state.set_state(Profile.gender)
        await message.answer(
            "Определимся с полом",
            reply_markup=await get_inline_buttons(
                btns={
                    "Я парень": "male",
                    "Я девушка": "female"
                }
            )
        )
    except ValueError as e:
        await message.answer(f"Ошибка, неверный возраст: {e}")


@router.message(Profile.city, F.text)
async def get_city(message: Message, state: FSMContext) -> None:
    """Принимает город пользователя, валидирует. Если валидация успешна, то вызывает состояние для приёма описания."""
    try:
        city = vld.UserCity(city=message.text)
        await vld.validate_city(city.city)
        await state.update_data(city=city.city)
        await state.set_state(Profile.description)
        await message.answer(text="Расскажи немного о себе.")
    except ValueError as e:
        await message.answer(f"Ошибка: {e}")


@router.message(Profile.description, F.text)
async def get_description(message: Message, state: FSMContext) -> None:
    """Принимает описания пользователя, валидирует. Если валидация успешна, то вызывает состояние для приёма фото."""
    if len(message.text) <= 255:
        await state.update_data(description=message.text)
        await state.set_state(Profile.photo_id)
        await message.answer(text="Отправь своё фото.")
    else:
        await message.answer("Описание не должно быть длиннее 255 символов.")


@router.message(Profile.photo_id, F.photo)
async def get_photo(message: Message, state: FSMContext,  bot: Bot) -> None:
    """Принимает фото пользователя и составляет анкету."""
    photo_sizes = message.photo
    if photo_sizes:
        photo = photo_sizes[-1]
        file_id = photo.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        downloaded_file = await bot.download_file(file_path)

        photo_path = f'{settings.FOLDER}/{message.from_user.id}.jpg'
        with open(photo_path, "wb") as f:
            f.write(downloaded_file.read())

        await state.update_data(photo_id=message.from_user.id)

        data = await state.get_data()
        name = data.get("name")
        age = data.get("age")
        city = data.get("city")
        description = data.get("description")

        text = (f"Так выглядит твоя анкета:\n"
                f"{name} - {age}, {city}\n"
                f"{description}")

        await bot.send_photo(
            chat_id=message.from_user.id,
            caption=text,
            photo=FSInputFile(photo_path)
        )
        await message.answer("Убедись, что всё верно.",
                             reply_markup=await get_inline_buttons(
                                 btns={
                                     "Да, всё верно": "profile_complete",
                                     "Нет, заполнить заново": "recreate_profile"
                                 }
                             ))






