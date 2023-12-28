from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from config import get_settings

# Создаем экземпляр MetaData
metadata = MetaData()

Base = declarative_base(metadata=metadata)

engine = create_async_engine(
    get_settings().database_sqlite_url,
    pool_pre_ping=True,  # Проверять соединение перед выполнением запроса
    pool_recycle=3600,  # Пересоздавать соединение каждый час
)

# Добавляем модели к метаданным
# metadata.reflect(bind=engine)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
