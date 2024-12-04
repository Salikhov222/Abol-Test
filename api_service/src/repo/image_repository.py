from sqlalchemy import select

from src.repo import BaseRepository
from src.models import Image as db_Image
from src.schema.image import ImageCreate
from src.exceptions import ImageNotFoundError


class ImageRepository(BaseRepository[db_Image]):
    
    async def get_image_by_user_id(self, image_id: int, user_id: int) -> db_Image | None:
        """Получение изображения по ID изображения и пользователя"""

        query = select(self.model).where(self.model.id == image_id, self.model.user_id == user_id)
        image = await self.session.execute(query)
        image = image.scalar_one_or_none()
        if not image:
            raise ImageNotFoundError(f'Изображение с ID {image_id} не найдено')
        return image
    
    async def get_all_images_by_user_id(self, user_id: int) -> list[db_Image]:
        """Получение всех изображений пользователя"""

        query = select(self.model).where(self.model.user_id == user_id)
        images = await self.session.execute(query)
        return images.scalars().all()
    
    async def add_image(self, image_data: ImageCreate, user_id: int) -> db_Image:
        """Добавление нового изображения"""
        
        image_db = db_Image(
            **image_data.model_dump(), 
            user_id=user_id
        )
        return await self.add(image_db)

    async def update_image_title(self, image_id: int, title: str, user_id: int) -> db_Image:
        """Обновление данных об изображении"""

        image = await self.get_image_by_user_id(image_id, user_id)
        if not image:
            raise ImageNotFoundError(f'Изображение с ID {image_id} не найдено')

        updated_image = await self.update(image.id, {"title": title})
        return updated_image
    
    async def delete_image(self, image_id: int, user_id: int) -> None:
        """Удаление изображения"""

        image = await self.get_image_by_user_id(image_id, user_id)
        if not image:
            raise ImageNotFoundError(f'Изображение с ID {image_id} не найдено')
        await self.delete(image.id)