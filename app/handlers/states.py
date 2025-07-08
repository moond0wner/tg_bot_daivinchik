"""
Модуль для хранения состояний пользователей.
"""

from aiogram.fsm.state import StatesGroup, State

class Profile(StatesGroup):
    name = State()
    age = State()
    gender = State()
    city = State()
    description = State()
    photo_id = State()

class Problem(StatesGroup):
    text_problem = State()