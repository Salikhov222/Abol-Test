from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class GoogleUserData(BaseModel):
    id: int
    email: str
    name: str
