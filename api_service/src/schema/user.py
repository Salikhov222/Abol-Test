from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_id: int
    username: str

class UserCreateClassic(BaseModel):
    username: str
    hashed_password: str

class UserCreateOAuth2(BaseModel):
    email: EmailStr
    name: str | None = None
    google_id: str | None = None
    yandex_id: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str