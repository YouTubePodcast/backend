from pydantic import BaseModel


class UserLogin(BaseModel):
    idToken: str


class UserToken(BaseModel):
    token: str
