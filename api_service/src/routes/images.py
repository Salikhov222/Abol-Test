from fastapi import APIRouter, File, UploadFile
from fixtures import data as fixtures_images
from src.models.images import Image


router = APIRouter(prefix="/images", tags=["images"])


@router.get(
        '/', 
        response_model=list[Image]
)
async def get_all_images():
    return fixtures_images

@router.post('/')
async def upload_file(file: UploadFile):
    return {'filename': file.filename}
