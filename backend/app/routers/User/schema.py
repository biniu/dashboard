from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    email: str
    username: str
    password: str
    is_active: bool
