from typing import Annotated

from fastapi import APIRouter, Depends

from src.schema import UserLogin, UserCreate
from src.service import UserService
from src.dependency import get_user_service


router = APIRouter(prefix="/user", tags=["user"])

@router.post(
    '/',
    response_model=UserLogin
)
async def create_user(
    body: UserCreate,
    user_repository: Annotated[UserService, Depends(get_user_service)]
) -> UserLogin:
    """Создание профиля пользователя"""
    return await user_repository.create_user(body.username, body.password)

