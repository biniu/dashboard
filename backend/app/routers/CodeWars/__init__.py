from .model import CodeWarsUser, CodeWarsUserStatistic, LanguageInfo, \
    LanguageScore
from .schema import CodeWarsUserSchema, CodeWarsUserStatisticSchema, \
    LanguageInfoSchema, LanguageScoreSchema

BASE_ROUTE = "CodeWars"


def register_routes(app, root="api"):
    from .controller import router as code_wars_router

    app.include_router(code_wars_router, prefix=f"/{root}/{BASE_ROUTE}")
