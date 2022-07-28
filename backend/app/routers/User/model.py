from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, Integer, String

from app.db import Base
from .schema import UserSchema


# todo move to utils
def get_password_hash(password):
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return bcrypt_context.hash(password)


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    @staticmethod
    def from_schema(user_schema: UserSchema):
        create_user_model = User()
        create_user_model.email = user_schema.email
        create_user_model.username = user_schema.username
        create_user_model.hashed_password = get_password_hash(
            user_schema.password)
        create_user_model.is_active = True

        return create_user_model
