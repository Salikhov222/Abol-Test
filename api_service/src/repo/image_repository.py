from src.repo import BaseRepository
from src.database.models import Image as db_Image
from src.schemas.image import Image
from src.exceptions import ImageNotFoundError


class ImageRepository(BaseRepository[db_Image]):
    
    async def get_image(self, image_id: int) -> db_Image:
        """Получение изображения по ID"""

        image = await self.get(image_id)
        if not image:
            raise ImageNotFoundError(f'Изображение с ID {image_id} не найдено')
        return image
    
    async def add_image(self, image_data: Image) -> db_Image:
        """Добавление нового изображения"""
        
        
        image_db = db_Image(**image_data.model_dump())
        return await self.add(image_db)

    async def update_image_title(self, image_id: int, title: str) -> db_Image:
        """Обновление данных об изображении"""

        image = await self.get(image_id)
        if not image:
            raise ImageNotFoundError(f'Изображение с ID {image_id} не найдено')

        updated_image = await self.update(image_id, {"title": title})
        return updated_image
    
    async def delete_image(self, image_id: int) -> None:
        """Удаление изображения"""

        image = await self.get(image_id)
        if not image:
            raise ImageNotFoundError(f'Изображение с ID {image_id} не найдено')
        await self.delete(image_id)