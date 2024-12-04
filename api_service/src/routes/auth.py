from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.schema import Token
from src.service import AuthService
from src.dependency import get_auth_service
from src.exceptions import UserNotCorrectPassword, UserNotFound


router = APIRouter(prefix='/auth', tags=["auth"])

@router.post(
    '/login',
    response_model=Token
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> Token:
    try:
        return await auth_service.login(form_data.username, form_data.password)
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UserNotCorrectPassword as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    