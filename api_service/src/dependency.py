from typing import Annotated
from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repo import BaseRepository
from src.database import get_session, base


def get_repo(model: type[base.Base]) -> Callable[[AsyncSession], BaseRepository]:
    """
    Фабрика зависимостей для создания репозитория

    Аргументы:
    - model (type[base.Base]): Класс модели SQLAlchemy, для которой создается репозиторий

    Возвращает:
    - Callable[[AsyncSession, BaseRepository]]: Функция-зависимость, которая принимает сессию и возвращает экземпляр репозитория,
    связанный с указанной моделью
    """
    def func(session: Annotated[AsyncSession, Depends(get_session)]):
        return BaseRepository(session, model)
    
    return func