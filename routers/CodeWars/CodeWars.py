from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from database import engine, SessionLocal

from routers.CodeWars import CodeWarsModels

router = APIRouter(
    prefix="/CodeWars",
    tags=["CodeWars"],
    responses={404: {"description": "Not found"}}
)


CodeWarsModels.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class CodeWarsUser(BaseModel):
    name: str


class CodeWarsUserStatistic(BaseModel):
    honor: int
    leaderboard_position: int
    kata_completed: int
    user_id: int


class LanguageInfo(BaseModel):
    name: str


class LanguageScore(BaseModel):
    score: int
    rank: int

    user_id: int
    lang_id: int


@router.get("/users")
async def read_users(db: Session = Depends(get_db)):
    return db.query(CodeWarsModels.CodeWarsUsers).all()


@router.post("/users")
async def create_user(user: CodeWarsUser, db: Session = Depends(get_db)):
    user_info_model = CodeWarsModels.CodeWarsUsers()
    user_info_model.name = user.name

    db.add(user_info_model)
    db.commit()

    return successful_response(201)


@router.get("/UserStatistics")
async def read_user_statistics(db: Session = Depends(get_db)):
    return db.query(CodeWarsModels.CodeWarsUserStatistics).all()


@router.post("/UserStatistics")
async def create_user_statistics(user_statistics: CodeWarsUserStatistic, db: Session = Depends(get_db)):
    user_statistics_model = CodeWarsModels.CodeWarsUserStatistics()
    user_statistics_model.honor = user_statistics.honor
    user_statistics_model.leaderboard_position = user_statistics.leaderboard_position
    user_statistics_model.kata_completed = user_statistics.kata_completed
    user_statistics_model.user_id = user_statistics.user_id

    db.add(user_statistics_model)
    db.commit()

    return successful_response(201)


@router.get("/LanguageInfos")
async def read_language_infos(db: Session = Depends(get_db)):
    return db.query(CodeWarsModels.LanguageInfos).all()


@router.post("/LanguageInfos")
async def create_language_infos(language_info: LanguageInfo, db: Session = Depends(get_db)):
    language_info_model = CodeWarsModels.LanguageInfos()
    language_info_model.name = language_info.name

    db.add(language_info_model)
    db.commit()

    return successful_response(201)


@router.get("/LanguageScores")
async def read_language_scores(db: Session = Depends(get_db)):
    return db.query(CodeWarsModels.LanguageScores).all()


@router.post("/LanguageScores")
async def create_language_scores(language_score: LanguageScore, db: Session = Depends(get_db)):
    language_score_model = CodeWarsModels.LanguageScores()
    language_score_model.score = language_score.score
    language_score_model.rank = language_score.rank
    language_score_model.user_id = language_score.user_id
    language_score_model.lang_id = language_score.lang_id

    db.add(language_score_model)
    db.commit()

    return successful_response(201)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }
