import aiofiles
import os

from datetime import datetime
from PIL import Image as pilImage
from fastapi import APIRouter, UploadFile
from fixtures import data as fixtures_images
from src.models.images import Image


router = APIRouter(prefix="/images", tags=["images"])


@router.get(
        '/', 
        response_model=list[Image]
)
async def get_all_images():
    return fixtures_images

@router.get('/{image_id}', response_model=Image)
async def get_image(image_id: int):
    for index, image in enumerate(fixtures_images):
        if image_id == image['id']:
            return fixtures_images[index]
    return {"message": 'Image not found'}

@router.post('/', response_model=Image)
async def upload_image(file: UploadFile):
    # сохранение файла на сервере
    file_location = f'src/uploads/{file.filename}'
    async with aiofiles.open(file_location, 'wb') as buffer:    # асинхронная запись файла
        await buffer.write(await file.read())
    
    # получение информации о разрешение изображения
    with pilImage.open(file_location) as img:
        width, height = img.size
    resolution = f'{width}x{height}'

    upload_date = datetime.now().date()
    size = os.path.getsize(file_location)

    return {
        'id': 1,
        'title': file.filename,
        'path_to_image': file_location,
        'upload_date': upload_date,
        'resolution': resolution,
        'size': size
        }

@router.patch('/{image_id}')
async def update_image(image_id: int, title: str):
    for image in fixtures_images:
        if image_id == image['id']:
            image['title'] = title
            return image
        
    return {'message': 'Image not found'}

@router.delete('/{image_id}')
async def delete_image(image_id: int):
    for index, image in enumerate(fixtures_images):
        if image_id == image['id']:
            del fixtures_images[index]
            return {'message': f'Image {image_id} successful delete'}
    return {'message': 'Image not found'}
