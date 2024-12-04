from typing import Optional

from datetime import date
from pydantic import BaseModel, ConfigDict


class Image(BaseModel):
    id: Optional[int] = None
    title: str
    path_to_image: str
    upload_date: date
    resolution: str
    size: int
    user_id: int 
    
    model_config = ConfigDict(from_attributes=True)


class ImageCreate(BaseModel):
    title: str
    path_to_image: str
    upload_date: date
    resolution: str
    size: int

    model_config = ConfigDict(from_attributes=True)