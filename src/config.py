from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

__all__ = [
    "config",
    "Config",
    "async_session_maker",
]

from src.models import Base


class Config(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATABASE_URL: str = "postgresql+asyncpg://admin:admin@localhost:5432/admin"


config = Config()
async_engine = create_async_engine(url=config.DATABASE_URL)
async_session_maker = async_sessionmaker(bind=async_engine)


# engine = create_engine(url=config.DATABASE_URL)
# Base.metadata.create_all(bind=engine)