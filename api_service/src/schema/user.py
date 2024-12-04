from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str

class UserInDB(BaseModel):
    username: str
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str