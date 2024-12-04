class ImageNotFoundError(Exception):
    pass

class CacheError(Exception):
    pass

class UserNotFound(Exception):
    detail = 'User not found'

class UserNotCorrectPassword(Exception):
    detail = 'User not correct password'

class TokenExpired(Exception):
    pass

class TokenNotCorrect(Exception):
    pass