from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.schema import UserLogin, UserCreate
from src.service import AuthService
from src.dependency import get_auth_service
from src.exceptions import UserNotCorrectPassword, UserNotFound


router = APIRouter(prefix='/auth', tags=["auth"])

@router.post(
    '/login',
    response_model=UserLogin
)
async def login(
    body: UserCreate,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserLogin:
    try:
        return await auth_service.login(body.username, body.password)
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    except UserNotCorrectPassword as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    