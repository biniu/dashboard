from datetime import date

from .schema import UserSchema, TokenSchema


def test_UserSchema_works():  # noqa
    user: UserSchema = UserSchema(
        **{
            "id": "1",
            "email": "bilbo@shire.com",
            "username": "Bilbo",
            "password": "very_secure_password",
            "is_active": True
        }
    )

    assert user.username == "Bilbo"
    assert user.email == "bilbo@shire.com"


def test_TokenSchema_works():  # noqa
    token: TokenSchema = TokenSchema(
        **{
            "access_token": "very_secure_token",
            "token_type": "bearer",
        }
    )

    assert token.access_token == "very_secure_token"
    assert token.token_type == "bearer"
