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
from src.client import YandexClient


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    password_service: PasswordService
    yandex_client: YandexClient


    async def login(self, username: str, password: str) -> Token:
        user = await self.user_repository.get_user_by_username(username)
        await self.validate_auth_user(user=user, password=password)
        access_token = await self.generate_access_token(user_id=user.id)
        return Token(access_token=access_token, token_type="bearer")
    
    async def validate_auth_user(self, user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFound('Пользователь не найден')
        if not self.password_service.verify_password(plain_password=password, hashed_password=user.hashing_password):
            raise UserNotCorrectPassword('Неверный пароль')
    
    async def generate_access_token(self, user_id: int) -> str:
        expires_data_unix = (datetime.now(timezone.utc) - timedelta(days=7)).timestamp()
        token = jwt.encode({'user_id': user_id, 'exp': expires_data_unix}, 
            self.settings.JWT_SECRET_KEY, 
            algorithm=self.settings.JWT_ENCODE_ALGORITHM
        )
        return token
    
    def get_user_id_from_access_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token=token, key=self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except JWTError as e:
            raise TokenNotCorrect('Нет токена авторизации или время жизни токена истекло')
        return payload['user_id']
    
    async def yandex_auth(self, code: str):
        user_data = self.yandex_client.get_user_info(code=code)
        print(user_data)

    async def get_yandex_redirect_url(self, redirect_uri: str) -> str:
        return self.settings.build_yandex_auth_url(redirect_uri=redirect_uri) 