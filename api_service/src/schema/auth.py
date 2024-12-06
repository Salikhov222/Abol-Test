from pydantic import BaseModel, Field, EmailStr


class YandexUserData(BaseModel):
    id: int
    login: str
    name: str = Field(alias='real_name')
    email: EmailStr = Field(alias='default_email')
    access_token: str