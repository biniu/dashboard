from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.routers.CodeWars import CodeWarsModels, CodeWarsUtils, CodeWarsSync
from app.routers.CodeWars.CodeWarsModels import CodeWarsUser, \
    CodeWarsUserStatistic, LanguageInfo, LanguageScore

router = APIRouter(
    prefix="/CodeWars",
    tags=["CodeWars"],
    responses={404: {"description": "Not found"}}
)

CodeWarsModels.Base.metadata.create_all(bind=engine)


@router.get("/sync")
async def sync(db: Session = Depends(get_db)):
    print("SYNC")
    CodeWarsSync.sync(db)
    return "OK"


@router.get("/users")
async def read_users(db: Session = Depends(get_db)):
    return CodeWarsUtils.get_users(db)


@router.post("/users")
async def create_user(user: CodeWarsUser, db: Session = Depends(get_db)):
    try:
        user_id = CodeWarsUtils.create_user(user, db)
    except HTTPException as ex:
        raise ex

    return {
        'status': 201,
        'transaction': 'Successful',
        'user_id': user_id
    }


@router.get("/UserStatistics/{user_id}")
async def read_user_statistics(user_id: int, db: Session = Depends(get_db)):
    try:
        return CodeWarsUtils.get_user_statistics(user_id, db)
    except HTTPException as ex:
        raise ex


@router.post("/UserStatistics/{user_id}")
async def create_user_statistics(user_id: int,
                                 user_statistics: CodeWarsUserStatistic,
                                 db: Session = Depends(get_db)):
    try:
        CodeWarsUtils.create_user_statistics(user_id, user_statistics, db)
        return successful_response(201)
    except HTTPException as ex:
        raise ex


@router.get("/LanguageInfos")
async def read_language_infos(db: Session = Depends(get_db)):
    return CodeWarsUtils.get_language_infos(db)


@router.post("/LanguageInfos")
async def create_language_infos(language_info: LanguageInfo,
                                db: Session = Depends(get_db)):
    try:
        lang_id = CodeWarsUtils.create_language_infos(language_info, db)
    except HTTPException as ex:
        raise ex

    return {
        'status': 201,
        'transaction': 'Successful',
        'id': lang_id
    }


@router.get("/LanguageScores/{user_id}")
async def read_language_scores(user_id: int, db: Session = Depends(get_db)):
    try:
        return CodeWarsUtils.get_languages_scores(user_id, db)
    except HTTPException as ex:
        raise ex


@router.get("/LanguageScores/{user_id}/{lang_id}")
async def read_language_scores(user_id: int, lang_id: int,
                               db: Session = Depends(get_db)):
    try:
        return CodeWarsUtils.get_language_scores(user_id, lang_id, db)
    except HTTPException as ex:
        raise ex


@router.post("/LanguageScores/{user_id}")
async def create_language_scores(user_id: int, language_score: LanguageScore,
                                 db: Session = Depends(get_db)):
    try:
        lang_score_id = CodeWarsUtils.create_language_scores(user_id,
                                                             language_score, db)
    except HTTPException as ex:
        raise ex

    return {
        'status': 201,
        'transaction': 'Successful',
        'id': lang_score_id
    }


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }
