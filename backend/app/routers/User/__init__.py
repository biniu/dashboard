from .model import User
from .schema import UserSchema

BASE_ROUTE = "User"


def register_routes(app, root="api"):
    from .controller import router as code_wars_router

    app.include_router(code_wars_router, prefix=f"/{root}/{BASE_ROUTE}")
