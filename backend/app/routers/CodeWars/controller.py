from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.routers.CodeWars import CodeWarsSync
from app.routers.CodeWars.service import CodeWarsService
from .schema import CodeWarsUserSchema, \
    CodeWarsUserStatisticSchema, LanguageInfoSchema, LanguageScoreSchema

router = APIRouter(
    prefix="/CodeWars",
    tags=["CodeWars"],
    responses={404: {"description": "Not found"}}
)


# router = APIRouter()


# CodeWarsModels.Base.metadata.create_all(bind=engine)


@router.get("/sync")
async def sync(db: Session = Depends(get_db)):
    print("SYNC")
    CodeWarsSync.sync(db)
    return "OK"


@router.get("/users")
async def read_users(db: Session = Depends(get_db)):
    return CodeWarsService.get_users(db)


@router.post("/users")
async def create_user(user: CodeWarsUserSchema, db: Session = Depends(get_db)):
    try:
        user_id = CodeWarsService.create_user(user, db)
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
        return CodeWarsService.get_user_statistics(user_id, db)
    except HTTPException as ex:
        raise ex


@router.post("/UserStatistics/{user_id}")
async def create_user_statistics(user_id: int,
                                 user_statistics: CodeWarsUserStatisticSchema,
                                 db: Session = Depends(get_db)):
    try:
        CodeWarsService.create_user_statistics(user_id, user_statistics, db)
        return successful_response(201)
    except HTTPException as ex:
        raise ex


@router.get("/LanguageInfos")
async def read_language_infos(db: Session = Depends(get_db)):
    return CodeWarsService.get_language_infos(db)


@router.post("/LanguageInfos")
async def create_language_infos(language_info: LanguageInfoSchema,
                                db: Session = Depends(get_db)):
    try:
        lang_id = CodeWarsService.create_language_infos(language_info, db)
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
        return CodeWarsService.get_languages_scores(user_id, db)
    except HTTPException as ex:
        raise ex


@router.get("/LanguageScores/{user_id}/{lang_id}")
async def read_language_scores(user_id: int, lang_id: int,
                               db: Session = Depends(get_db)):
    try:
        return CodeWarsService.get_language_scores(user_id, lang_id, db)
    except HTTPException as ex:
        raise ex


@router.post("/LanguageScores/{user_id}")
async def create_language_scores(user_id: int,
                                 language_score: LanguageScoreSchema,
                                 db: Session = Depends(get_db)):
    try:
        lang_score_id = CodeWarsService.create_language_scores(user_id,
                                                               language_score,
                                                               db)
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
