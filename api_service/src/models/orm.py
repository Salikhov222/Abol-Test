from sqlalchemy.orm import registry
from sqlalchemy import MetaData, Table, Column, Integer, String, Date
from schemas import images


metadata = MetaData()
mapper_reg = registry()

images = Table(
    'images', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=True),
    Column('path_to_image', String(255)),
    Column('upload_date', Date, nullable=False),
    Column('resolution', String(255), nullable=False),
    Column('size', Integer, nullable=False)
)

def start_mappers():
    lines_mapper = mapper_reg.map_imperatively(images.Image, images)    # Привязка класса модели к таблице
    