from typing import Annotated, Type
from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src.repo import BaseRepository, RedisCacheRepository, ImageRepository, UserRepository
from src.database import get_session, base
from src.models import Image, UserProfile
from src.cache import get_redis_connection
from src.service import ImageService, UserService, AuthService, PasswordService
from src.exceptions import TokenExpired, TokenNotCorrect
from src.config import app_settings
from src.client import YandexClient


def get_db_repo(
    model: type[base.Base],
    repo_class: Type[BaseRepository] = BaseRepository
) -> Callable[[AsyncSession], BaseRepository]:
    """
    Фабрика зависимостей для создания репозитория БД

    Аргументы:
    - model (type[base.Base]): Класс модели SQLAlchemy, для которой создается репозиторий
    - repo_class (Type[BaseRepository]): Класс репозитория (по умолчанию BaseRepository)
    Возвращает:
    - Callable[[AsyncSession, BaseRepository]]: Функция-зависимость, которая принимает сессию и возвращает экземпляр репозитория,
    связанный с указанной моделью
    """
    def func(session: Annotated[AsyncSession, Depends(get_session)]) -> BaseRepository:
        return repo_class(session=session, model=model)
    
    return func

def get_redis_repo(client: Redis = Depends(get_redis_connection)) -> RedisCacheRepository:
    """
    Функция-зависимость для создания репозитория работы с кэшем Redis
    """
    return RedisCacheRepository(client=client)

def get_image_service(
    image_repository: ImageRepository = Depends(get_db_repo(Image, ImageRepository)),
    image_cache: RedisCacheRepository = Depends(get_redis_repo)
) -> ImageService:
    """
    Функция создает и возвращает экземпляр сервиса ImageService
    Зависимости для репозитория и кэша загружаеются с помощью Depends

    Аргументы:
        image_repository (ImageRepository): репозиторий для работы с изображениями
        image_cache (RedisCacheRepository): репозиторий для работы с кэшем

    Возвращает:
        ImageService: экзепляр сервиса для работы с изображениями
    """
    return ImageService(
        image_repository=image_repository,
        image_cache=image_cache
    )

def get_password_service() -> PasswordService:
    return PasswordService()

def get_yandex_client() -> YandexClient:
    return YandexClient(settings=app_settings)

def get_auth_service(
    user_repository: UserRepository = Depends(get_db_repo(UserProfile, UserRepository)),
    password_service: PasswordService = Depends(get_password_service),
    yandex_client: YandexClient = Depends(get_yandex_client)
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=app_settings, 
        password_service=password_service,
        yandex_client=yandex_client
    )

def get_user_service(
    user_repository: UserRepository = Depends(get_db_repo(UserProfile, UserRepository)),
    auth_service: AuthService = Depends(get_auth_service),
    password_service: PasswordService = Depends(get_password_service)
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service, password_service=password_service)

security = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_id(
    token: Annotated[str, Depends(security)],
    auth_service: AuthService = Depends(get_auth_service)
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token=token)
        return user_id
    except TokenExpired as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except TokenNotCorrect as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
