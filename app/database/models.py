"""
Модуль для базы данных.
"""

from sqlalchemy import DateTime, String, BigInteger, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255))

class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column()
    gender: Mapped[str] = mapped_column(String(10))
    city: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(255))
    photo_id: Mapped[str] = mapped_column(String(255))


