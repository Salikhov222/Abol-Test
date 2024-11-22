from typing import Optional

from datetime import date
from pydantic import BaseModel


class Image(BaseModel):
    id: Optional[int] = None
    title: str
    path_to_image: str
    upload_date: date
    resolution: str
    size: int