from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db import get_db
# file with DB models
from .model import User
from .schema import UserSchema

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


class UserService:

    @staticmethod
    def get_password_hash(password):
        return bcrypt_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return bcrypt_context.verify(plain_password, hashed_password)

    # todo add exception for not found user
    @staticmethod
    async def get_user_by_id(user_id: int,
                             db: Session = Depends(get_db)) -> UserSchema:
        resp: UserSchema = db.query(User).filter(User.id == user_id).first()
        return UserSchema(**resp.__dict__)

    @staticmethod
    def authenticate_user(username: str, password: str,
                          db: Session = Depends(get_db)):
        user = db.query(User) \
            .filter(User.username == username) \
            .first()

        # todo: rise exception instead of return false
        if not user:
            return False
        if not UserService.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(username: str, user_id: int,
                            expires_delta: Optional[timedelta] = None):
        encode = {"sub": username, "id": user_id}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        encode.update({"exp": expire})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    async def get_current_user(
            token: str = Depends(oauth2_bearer),
            db: Session = Depends(get_db)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("id")
            if username is None or user_id is None:
                raise UserService.get_user_exception()
            user = await UserService.get_user_by_id(user_id, db)
            return user
        except JWTError:
            raise UserService.get_user_exception()

    @staticmethod
    def get_user_exception():
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    @staticmethod
    def get_token_exception():
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorret username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    @staticmethod
    def http_exception():
        return HTTPException(status_code=404, detail="Todo not found")
