from pathlib import Path

from pydantic import PostgresDsn, SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

__all__ = [
    "config",
    "Config",
    "async_session_maker",
]

MANAGE_APP_MIGRATIONS = [
    "shop",
]


class Config(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")
    DATABASE_URL: PostgresDsn
    SECRET_KEY: SecretStr


config = Config()
async_engine = create_async_engine(url=config.DATABASE_URL.unicode_string())
async_session_maker = async_sessionmaker(bind=async_engine)

