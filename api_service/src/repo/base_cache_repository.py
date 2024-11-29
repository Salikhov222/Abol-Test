from abc import ABC, abstractmethod
from typing import Any


class BaseCacheRepository(ABC):
    """
    Базовый интерфейс, который описывает общий контракт для любого инструмента кэширования
    """
    @abstractmethod
    async def get(self, key: str) -> Any:
        """Получить значение из кэша"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Установить значение в кэше с возможным временем жизни"""
        pass

    @abstractmethod
    async def invalidate(self, key: str) -> None:
        """Удалить значение из кэша"""
        pass