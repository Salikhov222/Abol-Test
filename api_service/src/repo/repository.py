from typing import Generic, TypeVar, Type, Optional, List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.base import Base
from src.schemas.image import Image


ModelType = TypeVar('ModelType', bound=Base)    # объявление переменной типа, привязанной к базовой модели Base

class BaseRepository(Generic[ModelType]):   # Generic - обобщенный тип данных для работы с различными моделями
    """ Базовый класс для работы с БД """

    def __init__(self, session: AsyncSession, model: Type[ModelType]) -> None:
        self.session = session
        self.model = model

    async def get(self, obj_id: int) -> Optional[ModelType]:
        """Получение одного объекта"""

        query = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def get_all(self) -> List[ModelType]:
        """Получение всех объектов"""

        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def add(self, obj: ModelType) -> ModelType:
        """Добавление нового объекта"""

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
        
    async def update(self, obj: ModelType) -> ModelType:
        """Обновление объекта"""

        await self.session.commit()
        await self.session.refresh()
        return obj

    async def delete(self, obj_id: int) -> None:
        """Удаление объекта"""

        query = delete(self.model).where(self.model.id == obj_id)
        await self.session.execute(query)
        await self.session.commit()
