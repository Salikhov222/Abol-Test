from datetime import date
from pydantic import BaseModel


class Image(BaseModel):
    id: int
    title: str
    path_to_image: str
    upload_date: date
    resolution: str
    size: int