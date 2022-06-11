from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.Habitica import HabiticaModels
from app.routers.Habitica.HabiticaModels import HabiticaUser, HabiticaTodo, HabiticaHabit, HabiticaDaily


def get_users(db: Session = Depends(get_db)):
    return db.query(HabiticaModels.HabiticaUsers).all()


def get_user_id(user: str, db: Session = Depends(get_db)) -> bool:
    return db.query(HabiticaModels.HabiticaUsers).filter(HabiticaModels.HabiticaUsers.name == user).first().id


def user_with_name_exist(user: str, db: Session = Depends(get_db)) -> bool:
    if db.query(HabiticaModels.HabiticaUsers).filter(HabiticaModels.HabiticaUsers.name == user).first():
        return True
    return False


def user_with_id_exist(user_id: int, db: Session = Depends(get_db)) -> bool:
    if db.query(HabiticaModels.HabiticaUsers).filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        return True
    return False


def create_user(user: HabiticaUser, db: Session = Depends(get_db)):
    if db.query(HabiticaModels.HabiticaUsers).filter(HabiticaModels.HabiticaUsers.name == user.name).first():
        raise HTTPException(status_code=400, detail="User already exists")

    user_info_model = HabiticaModels.HabiticaUsers()
    user_info_model.name = user.name

    db.add(user_info_model)
    db.commit()

    created_user = db.query(HabiticaModels.HabiticaUsers). \
        filter(HabiticaModels.HabiticaUsers.name == user.name) \
        .first()

    return created_user.id


def get_todos(user_id: int, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    todos = db.query(HabiticaModels.HabiticaTodos) \
        .filter(HabiticaModels.HabiticaTodos.user_id == user_id)
    return todos.all()


def create_todo(user_id: int, todo: HabiticaTodo, db: Session = Depends(get_db)):
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


def update_todo(user_id: int, todo: HabiticaTodo, db: Session = Depends(get_db)):
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


def delete_todo(user_id: int, habitica_id: str, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    todo_model = db.query(HabiticaModels.HabiticaTodos) \
        .filter(HabiticaModels.HabiticaTodos.habiticaID == habitica_id).first()

    if not todo_model:
        raise HTTPException(status_code=400, detail=f"Todo with habiticaID {habitica_id} NOT exist")

    db.query(HabiticaModels.HabiticaTodos) \
        .filter(HabiticaModels.HabiticaTodos.habiticaID == habitica_id) \
        .delete()

    db.commit()


def get_habits(user_id: int, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    habits = db.query(HabiticaModels.HabiticaHabits) \
        .filter(HabiticaModels.HabiticaHabits.user_id == user_id)
    return habits.all()


def create_habits(user_id: int, habit: HabiticaHabit, db: Session = Depends(get_db)):
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
    habit_model.priority = habit.priority
    habit_model.text = habit.text
    habit_model.user_id = user_id

    for elem in habit.history:
        history_entry = HabiticaModels.HabiticaHabitHistory()
        history_entry.date = elem.date
        history_entry.scoredUp = elem.scoredUp
        history_entry.scoredDown = elem.scoredDown

        habit_model.history.append(history_entry)

    db.add(habit_model)
    db.commit()


def update_habits(user_id: int, habit: HabiticaHabit, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    habit_model = db.query(HabiticaModels.HabiticaHabits) \
        .filter(HabiticaModels.HabiticaHabits.habiticaID == habit.habiticaID).first()

    if not habit_model:
        raise HTTPException(status_code=400, detail=f"Todo with habiticaID {habit.habiticaID} already exist")

    habit_model.habiticaID = habit.habiticaID
    habit_model.createdAt = habit.createdAt

    habit_model.up = habit.up
    habit_model.down = habit.down
    habit_model.counterUp = habit.counterUp
    habit_model.counterDown = habit.counterDown
    habit_model.frequency = habit.frequency
    habit_model.priority = habit.priority
    habit_model.text = habit.text
    habit_model.user_id = user_id

    for elem in habit.history:
        history_entry = HabiticaModels.HabiticaHabitHistory()
        history_entry.date = elem.date
        history_entry.scoredUp = elem.scoredUp
        history_entry.scoredDown = elem.scoredDown

        habit_model.history.append(history_entry)

    db.add(habit_model)
    db.commit()


def delete_habits(user_id: int, habitica_id: str, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    habit_model = db.query(HabiticaModels.HabiticaHabits) \
        .filter(HabiticaModels.HabiticaHabits.habiticaID == habitica_id).first()

    if not habit_model:
        raise HTTPException(status_code=400, detail=f"Todo with habiticaID {habitica_id} already exist")

    db.query(HabiticaModels.HabiticaHabits) \
        .filter(HabiticaModels.HabiticaHabits.habiticaID == habitica_id) \
        .delete()

    db.commit()


def get_dailies(user_id: int, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    dailies = db.query(HabiticaModels.HabiticaDailies) \
        .filter(HabiticaModels.HabiticaDailies.user_id == user_id)
    return dailies.all()


def create_daily(user_id: int, daily: HabiticaDaily, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    if db.query(HabiticaModels.HabiticaDailies) \
            .filter(HabiticaModels.HabiticaDailies.habiticaID == daily.habiticaID).first():
        raise HTTPException(status_code=400, detail=f"Todo with habiticaID {daily.habiticaID} already exist")

    daily_model = HabiticaModels.HabiticaDailies()
    daily_model.habiticaID = daily.habiticaID
    daily_model.createdAt = daily.createdAt

    daily_model.frequency = daily.frequency
    daily_model.everyX = daily.everyX
    daily_model.priority = daily.priority
    daily_model.text = daily.text

    daily_model.completed = daily.completed
    daily_model.isDue = daily.isDue
    daily_model.user_id = user_id

    for elem in daily.history:
        daily_entry = HabiticaModels.HabiticaDailiesHistory()
        daily_entry.date = elem.date
        daily_entry.due = elem.completed
        daily_entry.completed = elem.completed

        daily_model.history.append(daily_entry)

    db.add(daily_model)
    db.commit()


def update_daily(user_id: int, daily: HabiticaDaily, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    daily_model = db.query(HabiticaModels.HabiticaDailies) \
        .filter(HabiticaModels.HabiticaDailies.habiticaID == daily.habiticaID).first()

    if not daily_model:
        raise HTTPException(status_code=400, detail=f"Daily with habiticaID {daily.habiticaID} NOT exist")

    daily_model.habiticaID = daily.habiticaID
    daily_model.createdAt = daily.createdAt

    daily_model.frequency = daily.frequency
    daily_model.everyX = daily.everyX
    daily_model.priority = daily.priority
    daily_model.text = daily.text
    daily_model.isDue = daily.isDue

    daily_model.completed = daily.completed
    daily_model.user_id = user_id

    for elem in daily.history:
        daily_entry = HabiticaModels.HabiticaDailiesHistory()
        daily_entry.date = elem.date
        daily_entry.due = elem.completed
        daily_entry.completed = elem.completed

        daily_model.history.append(daily_entry)

    db.add(daily_model)
    db.commit()


def delete_daily(user_id: int, habitica_id: str, db: Session = Depends(get_db)):
    if not db.query(HabiticaModels.HabiticaUsers) \
            .filter(HabiticaModels.HabiticaUsers.id == user_id).first():
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} not exist")

    daily_model = db.query(HabiticaModels.HabiticaDailies) \
        .filter(HabiticaModels.HabiticaDailies.habiticaID == habitica_id).first()

    if not daily_model:
        raise HTTPException(status_code=400, detail=f"Daily with habiticaID {habitica_id} NOT exist")

    db.query(HabiticaModels.HabiticaDailies) \
        .filter(HabiticaModels.HabiticaDailies.habiticaID == habitica_id) \
        .delete()

    db.commit()
