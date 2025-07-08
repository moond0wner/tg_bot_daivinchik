"""
Модуль для запуска базы данных.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from redis.asyncio import Redis

from app.utils.config import settings

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

from .models import Base

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,
)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def start_db() -> None:
    """Запуск SQL БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)