from datetime import datetime, date
from enum import Enum
from pprint import pprint

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Json, validator

from typing import Optional, List

from database import engine, SessionLocal

from routers.Habitica import HabiticaModels

router = APIRouter(
    prefix="/Habitica",
    tags=["Habitica"],
    responses={404: {"description": "Not found"}}
)

HabiticaModels.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class HabiticaUser(BaseModel):
    name: str


class HabiticaTodo(BaseModel):
    habiticaID: str
    createdAt: datetime
    completedAt: Optional[datetime]
    completed: bool
    priority: int
    text: str


class Frequency(str, Enum):
    daily = 'daily'
    weekly = 'weekly'
    monthly = 'monthly'


class HabiticaHabitHistoryEntry(BaseModel):
    date: date
    scoredUp: int
    scoredDown: int

    class Config:
        orm_mode = True


class HabiticaHabit(BaseModel):
    habiticaID: str
    createdAt: datetime
    up: bool
    down: bool
    counterUp: int
    counterDown: int
    frequency: Frequency
    history: List[HabiticaHabitHistoryEntry] = []
    priority: int
    text: str

    class Config:
        orm_mode = True


@router.get("/users")
async def read_users(db: Session = Depends(get_db)):
    return db.query(HabiticaModels.HabiticaUsers).all()


@router.post("/users")
async def create_user(user: HabiticaUser, db: Session = Depends(get_db)):
    if db.query(HabiticaModels.HabiticaUsers).filter(HabiticaModels.HabiticaUsers.name == user.name).first():
        raise HTTPException(status_code=400, detail="User already exists")

    user_info_model = HabiticaModels.HabiticaUsers()
    user_info_model.name = user.name

    db.add(user_info_model)
    db.commit()

    created_user = db.query(HabiticaModels.HabiticaUsers). \
        filter(HabiticaModels.HabiticaUsers.name == user.name) \
        .first()

    print(created_user)

    return {
        'status': 201,
        'transaction': 'Successful',
        'user_id': created_user.id
    }


@router.get("/Todo/{user_id}")
async def read_todo(user_id: int, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    todos = db.query(HabiticaModels.HabiticaTodos) \
        .filter(HabiticaModels.HabiticaTodos.user_id == user_id)
    return todos.all()


@router.post("/Todo/{user_id}")
async def create_todo(user_id: int, todo: HabiticaTodo, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    if db.query(HabiticaModels.HabiticaTodos) \
            .filter(HabiticaModels.HabiticaTodos.habiticaID == todo.habiticaID).first():
        raise HTTPException(status_code=400, detail=f"Todo with habiticaID {todo.habiticaID} already exist")

    todo_model = HabiticaModels.HabiticaTodos()
    todo_model.habiticaID = todo.habiticaID
    todo_model.createdAt = todo.createdAt
    todo_model.completed = todo.completed
    todo_model.priority = todo.priority
    todo_model.text = todo.text
    todo_model.user_id = user_id

    db.add(todo_model)
    db.commit()

    return {
        'status': 201,
        'transaction': 'Successful'
    }


@router.put("/Todo/{user_id}")
async def update_todo(user_id: int, todo: HabiticaTodo, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    todo_model = db.query(HabiticaModels.HabiticaTodos) \
        .filter(HabiticaModels.HabiticaTodos.habiticaID == todo.habiticaID).first()

    if not todo_model:
        raise HTTPException(status_code=400, detail=f"Todo with habiticaID {todo.habiticaID} NOT exist")

    todo_model.habiticaID = todo.habiticaID
    todo_model.createdAt = todo.createdAt
    todo_model.completedAt = todo.completedAt
    todo_model.completed = todo.completed
    todo_model.priority = todo.priority
    todo_model.text = todo.text
    todo_model.user_id = user_id

    db.add(todo_model)
    db.commit()

    return {
        'status': 201,
        'transaction': 'Successful'
    }


@router.get("/Habits/{user_id}", response_model=List[HabiticaHabit])
async def read_habits(user_id: int, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    habits = db.query(HabiticaModels.HabiticaHabits) \
        .filter(HabiticaModels.HabiticaHabits.user_id == user_id)
    return habits.all()


@router.post("/Habits/{user_id}")
async def create_habits(user_id: int, habit: HabiticaHabit, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    if db.query(HabiticaModels.HabiticaHabits) \
            .filter(HabiticaModels.HabiticaHabits.habiticaID == habit.habiticaID).first():
        raise HTTPException(status_code=400, detail=f"Todo with habiticaID {habit.habiticaID} already exist")

    habit_model = HabiticaModels.HabiticaHabits()
    habit_model.habiticaID = habit.habiticaID
    habit_model.createdAt = habit.createdAt

    habit_model.up = habit.up
    habit_model.down = habit.down
    habit_model.counterUp = habit.counterUp
    habit_model.counterDown = habit.counterDown

    habit_model.frequency = habit.frequency
    # habit_model.history = habit.history

    habit_model.priority = habit.priority
    habit_model.text = habit.text
    habit_model.user_id = user_id

    # pprint(habit.history)

    for elem in habit.history:
        print(elem)
        history_entry = HabiticaModels.HabiticaHabitHistory()
        history_entry.date = elem.date
        history_entry.scoredUp = elem.scoreUp
        history_entry.scoredDown = elem.scoreDown

        habit_model.history.append(history_entry)

    print("habit_model.history")
    print(habit_model.history)

    db.add(habit_model)
    db.commit()

    return {
        'status': 201,
        'transaction': 'Successful'
    }
