class ImageNotFoundError(Exception):
    """Исключение, если изображение не найдено в БД"""
    pass

class CacheError(Exception):
    """Исключение для ошибок работы с кэшем"""
    pass

class UserNotFound(Exception):
    detail = 'User not found'

class UserNotCorrectPassword(Exception):
    detail = 'User not correct password'