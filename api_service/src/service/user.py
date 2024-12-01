from dataclasses import dataclass
import random
import string

from src.schema import UserLogin
from src.repo import UserRepository


@dataclass
class UserService:
    user_repository: UserRepository 

    async def create_user(self, username: str, password: str) -> UserLogin:
        access_token = await self._generate_access_token()
        user = await self.user_repository.create_user(username=username, password=password, access_token=access_token)
        return UserLogin(user_id=user.id, access_token=user.access_token)
    
    @staticmethod
    async def _generate_access_token() -> str:
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

