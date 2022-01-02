from fastapi import FastAPI
from routers.CodeWars import CodeWars


app = FastAPI()

app.include_router(CodeWars.router)
