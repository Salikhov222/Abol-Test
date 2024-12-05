from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
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
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except UserNotCorrectPassword as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    
@router.get(
    '/login/google',
    response_class=RedirectResponse
)
async def google_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> RedirectResponse:
    
    google_auth_url = await auth_service.get_google_redirect_url()
    print(google_auth_url)
    return RedirectResponse(url=google_auth_url)

@router.get(
    '/callback'
)
async def google_auth_callback(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
):
    return auth_service.google_auth(code=code)
