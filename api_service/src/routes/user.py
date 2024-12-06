from typing import Annotated

from fastapi import APIRouter, Depends

from src.schema import User, UserCreateClassic
from src.service import UserService
from src.dependency import get_user_service


router = APIRouter(prefix="/user", tags=["user"])

@router.post(
    '/',
    response_model=User
)
async def create_user(
    body: UserCreateClassic,
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> User:
    """Создание профиля пользователя"""

    return await user_service.create_user(body.username, body.hashed_password)

