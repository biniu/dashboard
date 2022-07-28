# from .model import User
# from .schema import UserSchema

BASE_ROUTE = "User"


def register_routes(app, root="api"):
    from .controller import router as user_router
    from .controller import token_router

    app.include_router(user_router, prefix=f"/{root}/{BASE_ROUTE}")
    app.include_router(token_router)
