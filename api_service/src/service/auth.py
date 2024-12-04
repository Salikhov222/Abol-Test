from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jose import jwt
from jose.exceptions import JWTError 

from src.schema import UserLogin
from src.repo import UserRepository
from src.models import UserProfile
from src.config import Settings
from src.exceptions import TokenNotCorrect, UserNotFound, UserNotCorrectPassword, TokenExpired

@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings 

    async def login(self, username: str, password: str) -> UserLogin:
        user = await self.user_repository.get_user_by_username(username)
        await self._validate_auth_user(user=user, password=password)
        access_token = await self.generate_access_token(user_id=user.id)
        return UserLogin(user_id=user.id, access_token=access_token)
    
    @staticmethod
    async def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFound
        if user.password != password:
            raise UserNotCorrectPassword
    
    async def generate_access_token(self, user_id: int) -> str:
        expires_data_unix = (datetime.now(timezone.utc) + timedelta(days=7)).timestamp()
        token = jwt.encode({'user_id': user_id, 'expire': expires_data_unix}, 
            self.settings.JWT_SECRET_KEY, 
            algorithm=self.settings.JWT_ENCODE_ALGORITHM
        )
        return token
    
    def get_user_id_from_access_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token=token, key=self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except JWTError as e:
            raise TokenNotCorrect('Нет токена авторизации')
        if payload['expire'] < datetime.now(timezone.utc).timestamp():
            raise TokenExpired('Время жизни токена истекло')
        return payload['user_id']