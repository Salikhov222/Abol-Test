from typing import Annotated, Optional

import aiofiles
import os

from datetime import datetime
from PIL import Image as pilImage
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fixtures import data as fixtures_images
from src.schemas.image import Image
from src.repo import BaseRepository, ImageRepository
from src.dependency import get_repo
from src.database import models as db_models, get_session


router = APIRouter(prefix="/images", tags=["images"])

ImageRepo = Annotated[
    BaseRepository[db_models.Image],
    Depends(get_repo(db_models.Image))
]   # указание возвращаемого типа для удобства

@router.get('/', response_model=list[Image])
async def get_all_images(repository: ImageRepo) -> list[Image]:
    images = await repository.get_all()
    return images

@router.get('/{image_id}', response_model=Image)
async def get_image(image_id: int, repository: ImageRepo) -> Optional[Image]:
    image = repository.get(image_id)
    if image:
        return image
    else:
        return {"message": 'Image not found'}

@router.post('/', response_model=Image)
async def upload_image(file: UploadFile, session: Annotated[AsyncSession, Depends(get_session)]):

    repository = ImageRepository(session=session, model=db_models.Image)
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
    await repository.add_image(image)
    return image

@router.patch('/{image_id}')
async def update_image(image_id: int, title: str, session: Annotated[AsyncSession, Depends(get_session)]): 
    repository = ImageRepository(session=session, model=db_models.Image)

    return await repository.update_image_title(image_id, title)

@router.delete('/{image_id}')
async def delete_image(image_id: int, repository: ImageRepo):
    await repository.delete(image_id)

    return {"message": f'Image {image_id} successfull delete'}
