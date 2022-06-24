import os

from fastapi import FastAPI

from app import create_app

app = FastAPI(title="Fasterific API")
create_app(app, config=os.getenv("ENV") or "test")
