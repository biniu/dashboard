from fastapi import Depends
from requests import Session

from app.database import get_db
from app.routers.Habitica import HabiticaUtils
from app.routers.Habitica.HabiticaModels import HabiticaUser, HabiticaTodo
from .HabiticaInterface import HabiticaInterface


def sync_todos(habitica_todos: list, dashboard_todos: list, user_id: int, db: Session = Depends(get_db)) -> None:
    for h_todo in habitica_todos:
        todo_exist = False
        for d_todo in dashboard_todos:
            if d_todo.habiticaID == h_todo.habiticaID:
                print("Todo already exist, check if need update")
                todo_exist = True
                if d_todo.priority == h_todo.priority \
                        and d_todo.text == h_todo.text \
                        and d_todo.completed == h_todo.completed:
                    print("Todo not change continue")
                    continue
                else:
                    print("Task updated")
                    HabiticaUtils.update_todo(
                        user_id=user_id,
                        todo=HabiticaTodo(
                            habiticaID=h_todo.habiticaID,
                            createdAt=h_todo.createdAt,
                            completedAt=h_todo.completedAt,
                            completed=h_todo.completed,
                            priority=h_todo.priority,
                            text=h_todo.text
                        ),
                        db=db
                    )
                    continue

        if not todo_exist:
            print("Creating todo")
            HabiticaUtils.create_todo(
                user_id=user_id,
                todo=HabiticaTodo(
                    habiticaID=h_todo.habiticaID,
                    createdAt=h_todo.createdAt,
                    completedAt=h_todo.completedAt,
                    completed=h_todo.completed,
                    priority=h_todo.priority,
                    text=h_todo.text
                ),
                db=db
            )


def remove_todos(habitica_todos: list, dashboard_todos: list, user_id: int, db: Session = Depends(get_db)) -> None:
    for d_todo in dashboard_todos:
        if d_todo.completed:
            continue
        todo_exist = False
        for h_todo in habitica_todos:
            if d_todo.habiticaID == h_todo.habiticaID:
                todo_exist = True
                break
        if not todo_exist:
            print(f"Todo to remove {d_todo.text}")
            HabiticaUtils.delete_todo(user_id, d_todo.habiticaID, db)


def sync_dailies(habitica_dailies: list, dashboard_dailies: list, user_id: int, db: Session = Depends(get_db)) -> None:
    for h_daily in habitica_dailies:
        daily_exist = False
        for d_daily in dashboard_dailies:
            if d_daily.habiticaID == h_daily.habiticaID:
                print("Daily already exist, check if need update")
                daily_exist = True
                if d_daily.frequency == h_daily.frequency \
                        and d_daily.everyX == h_daily.everyX \
                        and d_daily.priority == h_daily.priority \
                        and d_daily.text == h_daily.text \
                        and d_daily.completed == h_daily.completed \
                        and d_daily.isDue == h_daily.isDue \
                        and d_daily.history == h_daily.history:
                    print("Daily not change continue")
                    continue
                else:
                    print("Daily updated")
                    HabiticaUtils.update_daily(
                        user_id=user_id,
                        daily=h_daily,
                        db=db
                    )
                    continue

        if not daily_exist:
            print("Creating daily")
            HabiticaUtils.create_daily(
                user_id=user_id,
                daily=h_daily,
                db=db
            )


def sync_habits(habitica_habits: list, dashboard_habits: list, user_id: int, db: Session = Depends(get_db)) -> None:
    for h_habits in habitica_habits:
        habit_exist = False
        for d_habit in dashboard_habits:
            if d_habit.habiticaID == h_habits.habiticaID:
                print("Daily already exist, check if need update")
                habit_exist = True
                if d_habit.up == h_habits.up \
                        and d_habit.down == h_habits.down \
                        and d_habit.counterUp == h_habits.counterUp \
                        and d_habit.counterDown == h_habits.counterDown \
                        and d_habit.frequency == h_habits.frequency \
                        and d_habit.priority == h_habits.priority \
                        and d_habit.text == h_habits.text \
                        and d_habit.history == h_habits.history:
                    print("Daily not change continue")
                    continue
                else:
                    print("Daily updated")
                    HabiticaUtils.update_habits(
                        user_id=user_id,
                        habit=h_habits,
                        db=db
                    )
                    continue

        if not habit_exist:
            print("Creating daily")
            HabiticaUtils.create_habits(
                user_id=user_id,
                habit=h_habits,
                db=db
            )


def sync(db: Session = Depends(get_db)) -> None:
    user_name = 'biniu'

    habitica_client = HabiticaInterface()

    if HabiticaUtils.user_with_name_exist(user_name, db):
        print("User already exist")
        user_id = HabiticaUtils.get_user_id(user_name, db)
    else:
        print("Creating user")
        user_id = HabiticaUtils.create_user(user=HabiticaUser(name=user_name), db=db)

    print(f"user_id {user_id}")

    dashboard_todos = HabiticaUtils.get_todos(user_id, db)
    dashboard_dailies = HabiticaUtils.get_dailies(user_id, db)
    dashboard_habits = HabiticaUtils.get_habits(user_id, db)

    habitica_todos = habitica_client.get_todos()
    habitica_done_todos = habitica_client.get_done_todos()
    habitica_dailies = habitica_client.get_dailies()
    habitica_habits = habitica_client.get_habits()

    habitica_all_tasks = habitica_todos + habitica_done_todos

    print("Sync todos")
    sync_todos(habitica_todos, dashboard_todos, user_id, db)

    print("Sync done todos")
    sync_todos(habitica_done_todos, dashboard_todos, user_id, db)

    print("Remove todos")
    remove_todos(habitica_all_tasks, dashboard_todos, user_id, db)

    print("Sync dailies")
    sync_dailies(habitica_dailies, dashboard_dailies, user_id, db)

    print("Sync habits")
    sync_habits(habitica_habits, dashboard_habits, user_id, db)


if __name__ == '__main__':
    sync()
