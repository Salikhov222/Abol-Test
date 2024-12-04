from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base


class UserProfile(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashing_password: Mapped[str] = mapped_column(String, nullable=False)
