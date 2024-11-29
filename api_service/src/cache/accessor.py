from typing import AsyncGenerator

import redis.asyncio as redis

from src.config import redis_settings


async def get_redis_connection() -> AsyncGenerator[redis.Redis, None]:
    client =  redis.from_url(
        redis_settings.get_redis_url,
        decode_responses=True   # автоматическое преобразование данных в строку
    )

    try:
        yield client
    finally: 
        await client.close()

