from sqlalchemy import String, Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base


class Image(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    path_to_image: Mapped[str] = mapped_column(String, nullable=False)
    upload_date: Mapped[Date] = mapped_column(Date, nullable=False)
    resolution: Mapped[str] = mapped_column(String)
    size: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(ForeignKey('userprofile.id'), nullable=False)
