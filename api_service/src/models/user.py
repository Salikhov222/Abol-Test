from typing import Optional

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base


class UserProfile(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashing_password: Mapped[str] = mapped_column(String, nullable=False)
    google_access_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)