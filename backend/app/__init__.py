
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from .config import get_config
from .routes import register_routes


def create_app(app=None, config="dev"):
    if app is None:
        app = FastAPI(title="Fasterific API")

    settings = get_config(config=config)

    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_routes(app)

    @app.get("/")
    def index():
        return settings.CONFIG_NAME

    @app.get("/health")
    def health():
        return {"status": "healthy"}

    return app
