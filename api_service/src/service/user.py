from dataclasses import dataclass
import random
import string

from src.schema import UserLogin
from src.repo import UserRepository
from src.service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService  

    async def create_user(self, username: str, password: str) -> UserLogin:
        user = await self.user_repository.create_user(username=username, password=password)
        access_token = await self.auth_service.generate_access_token(user_id=user.id)
        return UserLogin(user_id=user.id, access_token=access_token)
