from datetime import timedelta

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import get_db
from .model import User
from .schema import UserSchema, TokenSchema
from .service import UserService

router = APIRouter(
    tags=["User"],
    responses={404: {"description": "Not found"}}
)

token_router = APIRouter(
    tags=["token"],
    responses={404: {"description": "Not found"}}
)


@router.post("/create")
async def create_new_user(create_user: UserSchema,
                          db: Session = Depends(get_db)):
    create_user_model = User()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.hashed_password = UserService.get_password_hash(
        create_user.password)
    create_user_model.is_active = True

    db.add(create_user_model)
    db.commit()


@router.get("/me", response_model=UserSchema)
async def read_users_me(
        current_user: UserSchema = Depends(
            UserService.get_current_user)):
    return current_user


@token_router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    user = UserService.authenticate_user(form_data.username, form_data.password,
                                         db)
    if not user:
        raise UserService.get_token_exception()
    token_expires = timedelta(minutes=20)
    token = UserService.create_access_token(user.username, user.id,
                                            expires_delta=token_expires)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/todo/{todo_id}")
async def read_todo(todo_id: int,
                    user: dict = Depends(UserService.get_current_user),
                    db: Session = Depends(get_db)):
    print("read_todo")
    if user is None:
        raise UserService.get_user_exception()
    out = [
        {"task": 1},
        {"task": 2},
        {"task": 3},
    ]
    if todo_id < len(out):
        return out[todo_id]
    raise UserService.http_exception()
