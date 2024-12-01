from dataclasses import dataclass

import aiofiles
import os
from datetime import datetime
from PIL import Image as pilImage
from fastapi import UploadFile

from src.repo import ImageRepository, RedisCacheRepository
from src.schema.image import Image


@dataclass
class ImageService:
    """
    Сервисная служба для CRUD-операций с изображениями
    """
    image_repository: ImageRepository
    image_cache: RedisCacheRepository

    async def get_all_images(self) -> list[Image]:
        cache_key = 'images'
        if images := await self.image_cache.get(cache_key):
            return images
    
        images = await self.image_repository.get_all()
        if not images:
            return []
        
        images_schema = [Image.model_validate(image) for image in images]
        await self.image_cache.set(cache_key, images_schema)
        return images
      
    async def get_image(self, image_id: int) -> Image:
        return await self.image_repository.get_image(image_id)
    

    async def upload_image(self, file: UploadFile) -> Image:
        cache_key = 'images'
        file_location = f'src/uploads/{file.filename}'  # сохранение файла на сервере
        async with aiofiles.open(file_location, 'wb') as buffer:    # асинхронная запись файла
            await buffer.write(await file.read())
        
        # получение информации о разрешение изображения
        with pilImage.open(file_location) as img:
            width, height = img.size
        resolution = f'{width}x{height}'

        upload_date = datetime.now().date()
        size = os.path.getsize(file_location)

        image = Image(
            title=file.filename, 
            path_to_image=file_location, 
            upload_date=upload_date, 
            resolution=resolution, 
            size=size
        )
        
        new_image = await self.image_repository.add_image(image)
        await self.image_cache.invalidate(cache_key)
        return new_image

    async def update_image(self, image_id: int, title: str) -> Image:
        cache_key = 'images'
        update_image = await self.image_repository.update_image_title(image_id, title)
        await self.image_cache.invalidate(cache_key)
        return update_image

    async def delete(self, image_id: int) -> None:
        cache_key = 'images'
        await self.image_repository.delete_image(image_id)
        await self.image_cache.invalidate(cache_key)


    