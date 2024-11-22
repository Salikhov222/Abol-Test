from collections.abc import AsyncGenerator

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from src.config import db_settings


engine = create_async_engine(
    db_settings.get_postgres_uri.unicode_string(),
    echo=True   # логирование запросов
    )

async_session = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)

# Функция для системы зависимостей Depends, которая устанавливает связь между логикой и конфигурацией БД
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise error

    