from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.routers.Habitica import HabiticaModels, HabiticaSync, HabiticaUtils
from app.routers.Habitica.HabiticaModels import HabiticaUser, HabiticaTodo, HabiticaHabit, HabiticaDaily

router = APIRouter(
    prefix="/Habitica",
    tags=["Habitica"],
    responses={404: {"description": "Not found"}}
)

HabiticaModels.Base.metadata.create_all(bind=engine)


@router.get("/sync")
async def sync(db: Session = Depends(get_db)):
    return HabiticaSync.sync(db)


@router.get("/users")
async def read_users(db: Session = Depends(get_db)):
    return HabiticaUtils.get_users(db)


@router.post("/users")
async def create_user(user: HabiticaUser, db: Session = Depends(get_db)):
    try:
        user_id = HabiticaUtils.create_user(user, db)
    except HTTPException as ex:
        raise ex

    return {
        'status': 201,
        'transaction': 'Successful',
        'user_id': user_id
    }


@router.get("/Todo/{user_id}")
async def read_todo(user_id: int, db: Session = Depends(get_db)):
    try:
        return HabiticaUtils.get_todos(user_id, db)
    except HTTPException as ex:
        raise ex


@router.post("/Todo/{user_id}")
async def create_todo(user_id: int, todo: HabiticaTodo, db: Session = Depends(get_db)):
    try:
        HabiticaUtils.create_todo(user_id, todo, db)
    except HTTPException as ex:
        raise ex

    return {
        'status': 201,
        'transaction': 'Successful'
    }


@router.put("/Todo/{user_id}")
async def update_todo(user_id: int, todo: HabiticaTodo, db: Session = Depends(get_db)):
    try:
        HabiticaUtils.update_todo(user_id, todo, db)
    except HTTPException as ex:
        raise ex

    return {
        'status': 201,
        'transaction': 'Successful'
    }


@router.delete("/Todo/{user_id}")
async def delete_todo(user_id: int, habitica_id: str, db: Session = Depends(get_db)):
    try:
        HabiticaUtils.delete_todo(user_id, habitica_id, db)
    except HTTPException as ex:
        raise ex

    return {
        'status': 201,
        'transaction': 'Successful'
    }


@router.get("/Habits/{user_id}", response_model=List[HabiticaHabit])
async def read_habits(user_id: int, db: Session = Depends(get_db)):
    try:
        return HabiticaUtils.get_habits(user_id, db)
    except HTTPException as ex:
        raise ex


@router.post("/Habits/{user_id}")
async def create_habits(user_id: int, habit: HabiticaHabit, db: Session = Depends(get_db)):
    try:
        HabiticaUtils.create_habits(user_id, habit, db)
    except HTTPException as ex:
        raise ex

    return {
        'status': 201,
        'transaction': 'Successful'
    }


@router.put("/Habits/{user_id}")
async def update_habits(user_id: int, habit: HabiticaHabit, db: Session = Depends(get_db)):
    try:
        HabiticaUtils.update_habits(user_id, habit, db)
    except HTTPException as ex:
        raise ex

    return {
        'status': 201,
        'transaction': 'Successful'
    }


@router.delete("/Habits/{user_id}")
async def delete_habits(user_id: int, habitica_id: str, db: Session = Depends(get_db)):
    try:
        HabiticaUtils.delete_habits(user_id, habitica_id, db)
    except HTTPException as ex:
        raise ex

    return {
        'status': 201,
        'transaction': 'Successful'
    }


@router.get("/Dailies/{user_id}", response_model=List[HabiticaDaily])
async def read_dailies(user_id: int, db: Session = Depends(get_db)):
    try:
        return HabiticaUtils.get_dailies(user_id, db)
    except HTTPException as ex:
        raise ex


@router.post("/Dailies/{user_id}")
async def create_dailies(user_id: int, daily: HabiticaDaily, db: Session = Depends(get_db)):
    try:
        HabiticaUtils.create_daily(user_id, daily, db)
    except HTTPException as ex:
        raise ex

    return {
        'status': 201,
        'transaction': 'Successful'
    }


@router.put("/Dailies/{user_id}")
async def update_dailies(user_id: int, daily: HabiticaDaily, db: Session = Depends(get_db)):
    try:
        HabiticaUtils.update_daily(user_id, daily, db)
    except HTTPException as ex:
        raise ex

    return {
        'status': 201,
        'transaction': 'Successful'
    }


@router.delete("/Dailies/{user_id}")
async def delete_dailies(user_id: int, habitica_id: str, db: Session = Depends(get_db)):
    try:
        HabiticaUtils.delete_daily(user_id, habitica_id, db)
    except HTTPException as ex:
        raise ex

    return {
        'status': 201,
        'transaction': 'Successful'
    }
