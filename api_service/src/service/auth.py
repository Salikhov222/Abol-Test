from dataclasses import dataclass

from src.schema import UserLogin
from src.repo import UserRepository
from src.models import UserProfile
from src.exceptions import UserNotFound, UserNotCorrectPassword

@dataclass
class AuthService:
    user_repository: UserRepository 

    async def login(self, username: str, password: str) -> UserLogin:
        user = await self.user_repository.get_user_by_username(username)
        await self._validate_auth_user(user=user, password=password)
        return UserLogin(user_id=user.id, access_token=user.access_token)
    
    @staticmethod
    async def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFound
        if user.password != password:
            raise UserNotCorrectPassword
    