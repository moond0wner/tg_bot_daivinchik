"""
Загрузка конфигурации из переменного окружения.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Загрузка переменных окружений и конвертация с помощью pydantic-settings."""
    BOT_TOKEN: str
    DATABASE_URL: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    DEVELOPER_ID: int
    FOLDER: str = "images"

    model_config = SettingsConfigDict()  # ../../../.env


settings = Settings()

