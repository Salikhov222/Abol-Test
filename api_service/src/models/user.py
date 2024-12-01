from sqlalchemy import String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base


class UserProfile(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    access_token: Mapped[str] = mapped_column(String, nullable=False)
