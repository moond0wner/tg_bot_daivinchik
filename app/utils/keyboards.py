"""
Модуль для работы с inline|reply клавиатурой.
"""

from aiogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

delete_kb = ReplyKeyboardRemove()

async def get_inline_buttons(
    *, btns: dict[str, str], sizes: tuple[int] = (2,)
) -> InlineKeyboardMarkup:
    """Конструктор inline клавиатуры."""
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


async def get_reply_buttons(
    *btns: str,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: tuple[int] = (2,),
) -> ReplyKeyboardMarkup:
    """Конструктор reply клавиатуры."""
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):

        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder
    )