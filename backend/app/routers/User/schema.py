from typing import Union

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    email: str
    username: str
    password: Union[str, None] = None
    is_active: bool


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
