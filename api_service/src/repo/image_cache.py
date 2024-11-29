import json
from redis.asyncio import Redis
from redis.exceptions import RedisError

from src.schemas.image import Image
from src.repo import BaseCacheRepository
from src.exceptions import CacheError


class RedisCacheRepository(BaseCacheRepository):
    def __init__(self, client: Redis) -> None:
        """
        Репозиторий для работы с Redis

        :param client: Redis клиент
        """
        self.client = client

    async def get(self, key: str) -> list[Image]:
        try:
            images_json = await self.client.lrange(key, 0, -1)
            return [Image.model_validate(json.loads(image)) for image in images_json]
        except RedisError as e:
            raise CacheError(f'Ошибка при получении данных из Redis по ключе {key}: {e}')
        
    async def set(self, key: str, value: list[Image], ttl: int = 3600) -> None:
        try:
            images_json = [image.model_dump_json() for image in value]
            await self.client.lpush(key, *images_json)
            await self.client.ltrim(key, 0, 99)
            await self.client.expire(key, ttl)
        except RedisError as e:
            raise CacheError(f'Ошибка при вставке данных в Redis по ключу {key}: {e}')

    async def invalidate(self, key: str) -> None:
        try:
            await self.client.delete(key)
        except RedisError as e:
            raise CacheError(f'Ошибка при удалении данных из Redis по клюу {key}: {e}')