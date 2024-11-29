class ImageNotFoundError(Exception):
    """Исключение, если изображение не найдено в БД"""
    pass

class CacheError(Exception):
    """Исключение для ошибок работы с кэшем"""
    pass