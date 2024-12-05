from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jose import jwt
from jose.exceptions import JWTError 

from src.schema import Token
from src.repo import UserRepository
from src.models import UserProfile
from src.config import Settings
from src.exceptions import TokenNotCorrect, UserNotFound, UserNotCorrectPassword
from src.service.password_service import PasswordService
from src.client import GoogleClient


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    password_service: PasswordService
    google_client: GoogleClient


    def google_auth(self, code: str):
        user_data = self.google_client.get_user_info(code=code)
        self.user_repository.create_user

    async def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    async def login(self, username: str, password: str) -> Token:
        user = await self.user_repository.get_user_by_username(username)
        await self.validate_auth_user(user=user, password=password)
        access_token_expires = timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await self.create_access_token(data={'user_id': user.id}, expires_delta=access_token_expires)
        return Token(access_token=access_token, token_type='bearer')
    
    async def validate_auth_user(self, user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFound('Пользователь не найден')
        if not self.password_service.verify_password(plain_password=password, hashed_password=user.hashing_password):
            raise UserNotCorrectPassword('Неверный пароль')
    
    async def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expires_data_unix = (datetime.now(timezone.utc) + expires_delta).timestamp()
        else:
            expires_data_unix = (datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp()
        to_encode.update({'exp': expires_data_unix})
        token = jwt.encode(
            to_encode, 
            self.settings.JWT_SECRET_KEY, 
            algorithm=self.settings.JWT_ENCODE_ALGORITHM
        )
        return token

    def get_user_id_from_access_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token=token, key=self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
            user_id: int = payload.get('user_id')
            if user_id is None:
                raise TokenNotCorrect('Не удалось проверить учетные данные')
        except JWTError as e:
            raise TokenNotCorrect('Нет токена авторизации или время жизни токена истекло')
        return user_id