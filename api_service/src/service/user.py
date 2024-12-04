from dataclasses import dataclass
import random
import string

from src.schema import User
from src.repo import UserRepository
from src.service.auth import AuthService
from src.service.password_service import PasswordService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService 
    password_service: PasswordService


    async def create_user(self, username: str, password: str) -> User:
        hashed_password = self.password_service.get_password_hash(password=password)
        user = await self.user_repository.create_user(username=username, password=hashed_password)
        access_token = await self.auth_service.generate_access_token(user_id=user.id)
        return User(user_id=user.id, username=user.username)
