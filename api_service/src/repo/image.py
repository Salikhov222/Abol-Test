from sqlalchemy import update

from src.repo import BaseRepository
from src.database.models import Image as db_Image
from src.schemas.image import Image


class ImageRepository(BaseRepository[db_Image]):
    async def add_image(self, image_data: Image) -> db_Image:
        """Добавление нового изображения"""
        
        image_db = db_Image(**image_data.model_dump())
        self.session.add(image_db)
        await self.session.commit()
        await self.session.refresh(image_db)
        return image_db

    async def update_image_title(self, image_id: int, title: str) -> db_Image:
        query = update(db_Image).where(db_Image.id == image_id).values(title=title).returning(db_Image.id)
        result = await self.session.execute(query)
        return await self.get(result.scalar_one_or_none())