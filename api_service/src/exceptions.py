class ImageNotFoundError(Exception):
    pass

class CacheError(Exception):
    pass

class UserNotFound(Exception):
    pass

class UserNotCorrectPassword(Exception):
    pass

class TokenExpired(Exception):
    pass

class TokenNotCorrect(Exception):
    pass