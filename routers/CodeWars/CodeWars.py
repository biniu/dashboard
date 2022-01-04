from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from typing import Optional

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

    last_update: Optional[date]


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
    if db.query(CodeWarsModels.CodeWarsUsers).filter(CodeWarsModels.CodeWarsUsers.name == user.name).first():
        raise HTTPException(status_code=400, detail="User already exists")

    user_info_model = CodeWarsModels.CodeWarsUsers()
    user_info_model.name = user.name

    db.add(user_info_model)
    db.commit()

    created_user = db.query(CodeWarsModels.CodeWarsUsers).\
        filter(CodeWarsModels.CodeWarsUsers.name == user.name)\
        .first()

    print(created_user)

    return {
        'status': 201,
        'transaction': 'Successful',
        'user_id': created_user.id
    }


@router.get("/UserStatistics/{user_id}")
async def read_user_statistics(user_id: int, db: Session = Depends(get_db)):
    if not db.query(CodeWarsModels.CodeWarsUsers) \
            .filter(CodeWarsModels.CodeWarsUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    user_statistics = db.query(CodeWarsModels.CodeWarsUserStatistics) \
        .filter(CodeWarsModels.CodeWarsUserStatistics.user_id == user_id)
    return user_statistics.all()


@router.post("/UserStatistics/{user_id}")
async def create_user_statistics(user_id: int, user_statistics: CodeWarsUserStatistic, db: Session = Depends(get_db)):
    print("create_user_statistics")

    if not db.query(CodeWarsModels.CodeWarsUsers) \
            .filter(CodeWarsModels.CodeWarsUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    if user_statistics.last_update:
        print("data from parm")
        statistic_date = user_statistics.last_update
    else:
        print("create new date")
        statistic_date = datetime.today().strftime('%Y-%m-%d')

    print("*"*80)
    print(repr(statistic_date))
    print("*" * 80)

    last_update = db.query(CodeWarsModels.CodeWarsUserStatistics) \
        .filter(CodeWarsModels.CodeWarsUserStatistics.last_update == statistic_date)

    if last_update.first():
        print(f"User statistic for {statistic_date} exist -> update exist one")
        user_statistics_model = last_update.first()
    else:
        print(f"User statistic for {statistic_date} not exist -> create new one")
        user_statistics_model = CodeWarsModels.CodeWarsUserStatistics()
    user_statistics_model.honor = user_statistics.honor
    user_statistics_model.leaderboard_position = user_statistics.leaderboard_position
    user_statistics_model.kata_completed = user_statistics.kata_completed
    user_statistics_model.user_id = user_id

    if user_statistics.last_update:
        user_statistics_model.last_update = statistic_date

    db.add(user_statistics_model)
    db.commit()

    return successful_response(201)


@router.get("/LanguageInfos")
async def read_language_infos(db: Session = Depends(get_db)):
    return db.query(CodeWarsModels.LanguageInfos).all()


@router.post("/LanguageInfos")
async def create_language_infos(language_info: LanguageInfo, db: Session = Depends(get_db)):
    if db.query(CodeWarsModels.LanguageInfos).filter(CodeWarsModels.LanguageInfos.name == language_info.name).first():
        raise HTTPException(status_code=400, detail=f"Language {language_info.name} already exists")

    language_info_model = CodeWarsModels.LanguageInfos()
    language_info_model.name = language_info.name

    db.add(language_info_model)
    db.commit()

    created_language = db.query(CodeWarsModels.LanguageInfos).\
        filter(CodeWarsModels.LanguageInfos.name == language_info.name)\
        .first()

    print(created_language)

    return {
        'status': 201,
        'transaction': 'Successful',
        'user_id': created_language.id
    }



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
