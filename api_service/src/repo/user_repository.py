from sqlalchemy import insert, select

from src.repo import BaseRepository
from src.models.user import UserProfile as db_User
from src.schema import UserLogin

class UserRepository(BaseRepository[db_User]):

    async def create_user(self, username: str, password: str) -> db_User:
        query = insert(db_User).values(
            username=username, 
            password=password
        ).returning(db_User.id)
        result = await self.session.execute(query)
        user_id = result.scalar()
        await self.session.commit()
        await self.session.flush()
        return await self.get_user(user_id)

    
    async def get_user(self, user_id: int) -> db_User | None:
        query = select(db_User).where(db_User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> db_User | None:
        query = select(db_User).where(db_User.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()