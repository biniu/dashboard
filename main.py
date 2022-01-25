from fastapi import FastAPI
from routers.CodeWars import CodeWars
from routers.Habitica import Habitica


app = FastAPI()

app.include_router(CodeWars.router)
app.include_router(Habitica.router)
