from pytest import fixture

from app.db import Session
from app.test.fixtures import app, session  # noqa
from .model import User
from .schema import UserSchema


@fixture
def user() -> UserSchema:
    user_schema = UserSchema(
        id=1,
        email="Frodo@shire.com",
        username="Frodo",
        password="very_secure_password",
        is_active=True
    )
    return User.from_schema(user_schema)


def test_User_create(user):  # noqa
    assert user


def test_User_retrieve(user,  # noqa
                       session: Session):
    session.add(user)
    session.commit()
    s = session.query(User).first()
    assert s.__dict__ == user.__dict__
