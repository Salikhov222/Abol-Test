from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends, HTTPException, status

from src.schema.image import Image
from src.dependency import get_image_service, get_current_user_id
from src.service import ImageService
from src.exceptions import ImageNotFoundError, CacheError


router = APIRouter(prefix="/images", tags=["images"])

@router.get(
    '/', 
    response_model=list[Image]
)
async def get_all_images(
    image_service: Annotated[ImageService, Depends(get_image_service)],
    user_id: int = Depends(get_current_user_id)
) -> list[Image]:
    """Получение информации о всех изображениях""" 
    try:
        return await image_service.get_all_images(user_id=user_id)
    except CacheError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка кэша: {str(e)}'
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения изображений: {str(e)}"
        )

@router.get(
    '/{image_id}',
    response_model=Image
)
async def get_image(
    image_id: int,
    image_service: Annotated[ImageService, Depends(get_image_service)],
    user_id: int = Depends(get_current_user_id)
) -> Image:
    """Получение информации об определенном изображении"""
    try:
        return await image_service.get_image_by_user_id(image_id=image_id, user_id=user_id)
    except ImageNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post(
    '/', 
    response_model=Image,
    status_code=status.HTTP_201_CREATED
)
async def upload_image(
    file: UploadFile,
    image_service: Annotated[ImageService, Depends(get_image_service)],
    user_id: int = Depends(get_current_user_id) 
) -> Image:
    """Загрузка нового изображения"""
    try:
        return await image_service.upload_image(file=file, user_id=user_id)
    except IOError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка сохранения файла: {str(e)}'
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.patch(
    '/{image_id}',
    response_model=Image
)
async def update_image(
    image_id: int, 
    title: str, 
    image_service: Annotated[ImageService, Depends(get_image_service)],
    user_id: int = Depends(get_current_user_id)
) -> Image:
    """Обновление названия изображения"""
    try:
        return await image_service.update_image(image_id=image_id, title=title, user_id=user_id)
    except ImageNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    '/{image_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_image(
    image_id: int, 
    image_service: Annotated[ImageService, Depends(get_image_service)],
    user_id: int = Depends(get_current_user_id)
):
    """Удаление конкретного изображения"""  
    try:
        return await image_service.delete(image_id=image_id, user_id=user_id)
    except ImageNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )