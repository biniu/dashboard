from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers.CodeWars import CodeWars
from app.routers.Habitica import Habitica


app = FastAPI()

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

app.include_router(CodeWars.router)
app.include_router(Habitica.router)


@app.get("/")
async def i_am_alive():
    return {"I'm alive!!!!!!!"}
