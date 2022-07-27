from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, status, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
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

router = APIRouter(
    prefix="/User",
    tags=["User"],
    responses={404: {"description": "Not found"}}
)


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(User) \
        .filter(User.username == username) \
        .first()

    # todo: rise exception instead of return false
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()


@router.post("/create/user")
async def create_new_user(create_user: UserSchema,
                          db: Session = Depends(get_db)):
    create_user_model = User()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.hashed_password = get_password_hash(create_user.password)
    create_user_model.is_active = True

    db.add(create_user_model)
    db.commit()


@router.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise get_token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id,
                                expires_delta=token_expires)
    return {"token": token}



@router.get("/todo/{todo_id}")
async def read_todo(todo_id: int,
                    user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    out = [
        {"task": 1},
        {"task": 2},
        {"task": 3},
    ]
    if todo_id < len(out):
        return out[todo_id]
    raise http_excetion()




def get_user_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )


def get_token_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorret username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )


def http_excetion():
    return HTTPException(status_code=404, detail="Todo not found")


def sucesful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }