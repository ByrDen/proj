import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import PostgresDsn, SecretStr, Field
from pydantic_settings import BaseSettings
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
    DATABASE_URL: PostgresDsn = f'{os.getenv("DATABASE_URL")}'
    SECRET_KEY: SecretStr = os.getenv("SECRET_KEY")


load_dotenv()
config = Config()
async_engine = create_async_engine(url=config.DATABASE_URL.unicode_string())
async_session_maker = async_sessionmaker(bind=async_engine)

