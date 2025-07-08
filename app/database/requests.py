"""
Модуль для обращения к базе данных.
"""

import logging
import random
from typing import Optional

from sqlalchemy import select, and_, or_

from app.database.engine import async_session, redis
from app.database.models import User, Profile


async def set_user(tg_id: int, username: str) -> None:
    """Добавляет пользователя в базу данных"""
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            
            if not user:
                session.add(User(tg_id=tg_id, username=username))
                await session.commit()
                logging.info("Добавлен новый пользователь %s (%s)", username, tg_id)
                
        except Exception as e:
            logging.error("Ошибка при добавлении пользователя %s (%s): %s", username, tg_id, str(e))


async def check_profile(tg_id: int) -> bool:
    """Проверка на наличие анкеты пользователя через айди его аккаунта."""
    async with async_session() as session:
        try:
            profile = await session.scalar(select(Profile).where(Profile.tg_id == tg_id))
            return True if profile else False
        except Exception as e:
            logging.error("Ошибка в check_profile: %s", str(e))


async def create_profile(
        tg_id: int,
        name: str,
        age: int,
        gender: str,
        city: str,
        description: str,
        photo_id: str
) -> None:
    """Создаёт анкету для знакомств в базе данных."""
    async with async_session() as session:
        new_profile = Profile(
            tg_id=tg_id,
            name=name,
            age=age,
            gender=gender,
            city=city,
            description=description,
            photo_id=photo_id
        )
        session.add(new_profile)
        await session.commit()


async def get_profile(tg_id: int) -> Profile:
    """Возвращает экземпляр модели базы данных Profile с которой можно взаимодействовать с помощью атрибутов."""
    async with async_session() as session:
        profile = await session.scalar(select(Profile).where(Profile.tg_id == tg_id))
        return profile


async def get_random_profile(tg_id: int) -> Optional[Profile]:
    """Выдаёт случайную анкету из БД по определенным критериям.
    Сохраняет айди уже отсмотренных профилей в Redis.
    Если длина списка случайных профилей и длина массива из Redis совпадает, то считается что все анкеты отсмотрены."""
    key = f"user_{tg_id}"
    async with async_session() as session:
        user_profile = await session.scalar(select(Profile).where(Profile.tg_id == tg_id))
        while True:
            target_profiles = await session.scalars(
                select(Profile).where(
                    and_(
                        Profile.tg_id != tg_id, # Пользователю не нужна его же анкета
                        Profile.city == user_profile.city, # Ищем анкету по городу пользователя
                        Profile.gender != user_profile.gender, # Для мальчика - девочку, для девочку - мальчика
                        or_( # Возраст такой же или старше/младше на год (не больше, не меньше)
                            Profile.age == user_profile.age,
                            Profile.age == user_profile.age - 1,
                            Profile.age == user_profile.age + 1
                        )
                    )
                )
            )
            profile_list = target_profiles.all()
            if not profile_list:
                logging.info("Нет доступных профилей")
                return None

            random_profile: Profile = random.choice(profile_list)
            if not random_profile:
                logging.info("Нет доступных профилей")
                return None

            redis_array_length = await redis.scard(key)
            if redis_array_length == len(profile_list):
                logging.info("Все профили закончились!")
                await redis.delete(key)
                return None

            if not await redis.sismember(key, random_profile.tg_id):
                await redis.sadd(key, random_profile.tg_id)
                return random_profile
            else:
                logging.info("Профиль %d уже был показан. Подбираем другой...", random_profile.tg_id)

