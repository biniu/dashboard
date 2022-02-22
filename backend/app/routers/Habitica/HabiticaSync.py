from pprint import pprint

import requests
import json
from HabiticaInterface import HabiticaInterface


def data_get(url: str):
    with requests.Session() as session:
        session = requests.Session()
        response = session.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Request failed!")
        print(response.status_code)
        print(response.reason)
        pprint(response.json())
        raise requests.HTTPError


def data_post(url: str, data: json):
    with requests.Session() as session:
        session = requests.Session()
        response = session.post(url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print("Request failed!")
        print(response.status_code)
        print(response.reason)
        pprint(response.json())
        raise requests.HTTPError


def data_put(url: str, data: json):
    with requests.Session() as session:
        session = requests.Session()
        response = session.put(url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print("Request failed!")
        print(response.status_code)
        print(response.reason)
        pprint(response.json())
        raise requests.HTTPError


def sync_todos(habitica_todos: list, dashboard_todos: list, user_id: int) -> None:
    for h_todo in habitica_todos:
        todo_exist = False
        for d_todo in dashboard_todos:
            if d_todo['habiticaID'] == h_todo.habiticaID:
                print("Todo already exist, check if need update")
                todo_exist = True
                if d_todo['priority'] == h_todo.priority \
                        and d_todo['text'] == h_todo.text \
                        and d_todo['completed'] == h_todo.completed:
                    print("Todo not change continue")
                    continue
                else:
                    print("Task updated")
                    data_put(
                        url=f"http://127.0.0.1:8000/Habitica/Todo/{user_id}",
                        data={
                            "habiticaID": h_todo.habiticaID,
                            "createdAt": h_todo.createdAt,
                            "completedAt": h_todo.completedAt,
                            "completed": h_todo.completed,
                            "priority": h_todo.priority,
                            "text": h_todo.text
                        }
                    )
                    continue

        if not todo_exist:
            print("Creating todo")
            data_post(
                url=f"http://127.0.0.1:8000/Habitica/Todo/{user_id}",
                data={
                    "habiticaID": h_todo.habiticaID,
                    "createdAt": h_todo.createdAt,
                    "completedAt": h_todo.completedAt,
                    "completed": h_todo.completed,
                    "priority": h_todo.priority,
                    "text": h_todo.text
                }
            )


def sync_dailies(habitica_dailies: list, dashboard_dailies: list, user_id: int) -> None:
    for h_daily in habitica_dailies:
        daily_exist = False
        for d_daily in dashboard_dailies:
            if d_daily['habiticaID'] == h_daily.habiticaID:
                print("Daily already exist, check if need update")
                daily_exist = True
                if d_daily['frequency'] == h_daily.frequency \
                        and d_daily['everyX'] == h_daily.everyX \
                        and d_daily['priority'] == h_daily.priority \
                        and d_daily['text'] == h_daily.text \
                        and d_daily['completed'] == h_daily.completed \
                        and d_daily['isDue'] == h_daily.isDue \
                        and d_daily['history'] == h_daily.history:
                    print("Daily not change continue")
                    continue
                else:
                    print("Daily updated")
                    data_put(
                        url=f"http://127.0.0.1:8000/Habitica/Dailies/{user_id}",
                        data=json.loads(h_daily.to_json())
                    )
                    continue

        if not daily_exist:
            print("Creating daily")
            data_post(
                url=f"http://127.0.0.1:8000/Habitica/Dailies/{user_id}",
                data=json.loads(h_daily.to_json())
            )


def sync_habits(habitica_habits: list, dashboard_habits: list, user_id: int) -> None:
    for h_habits in habitica_habits:
        habit_exist = False
        for d_habit in dashboard_habits:
            if d_habit['habiticaID'] == h_habits.habiticaID:
                print("Daily already exist, check if need update")
                habit_exist = True
                if d_habit['up'] == h_habits.up \
                        and d_habit['down'] == h_habits.down \
                        and d_habit['counterUp'] == h_habits.counterUp \
                        and d_habit['counterDown'] == h_habits.counterDown \
                        and d_habit['frequency'] == h_habits.frequency \
                        and d_habit['priority'] == h_habits.priority \
                        and d_habit['text'] == h_habits.text \
                        and d_habit['history'] == h_habits.history:
                    print("Daily not change continue")
                    continue
                else:
                    print("Daily updated")
                    print(h_habits.to_json())
                    data_put(
                        url=f"http://127.0.0.1:8000/Habitica/Habits/{user_id}",
                        data=json.loads(h_habits.to_json())
                    )
                    continue

        if not habit_exist:
            print("Creating daily")
            data_post(
                url=f"http://127.0.0.1:8000/Habitica/Habits/{user_id}",
                data=json.loads(h_habits.to_json())
            )


def sync() -> None:
    user_name = 'biniu'

    habitica_client = HabiticaInterface()

    users = data_get(url="http://127.0.0.1:8000/Habitica/users")
    user_exist = list(filter(lambda user: user['name'] == user_name, users))

    if user_exist:
        print("User already exist")
        user_id = user_exist[0]['id']
    else:
        print("Creating user")
        data = data_post(url="http://127.0.0.1:8000/Habitica/users", data={"name": user_name})
        user_id = data['user_id']

    print(f"user_id {user_id}")

    dashboard_todos = data_get(url=f"http://127.0.0.1:8000/Habitica/Todo/{user_id}")
    dashboard_dailies = data_get(url=f"http://127.0.0.1:8000/Habitica/Dailies/{user_id}")
    dashboard_habits = data_get(url=f"http://127.0.0.1:8000/Habitica/Habits/{user_id}")
    habitica_todos = habitica_client.get_todos()
    habitica_done_todos = habitica_client.get_done_todos()
    habitica_dailies = habitica_client.get_dailies()
    habitica_habits = habitica_client.get_habits()

    print("Sync todos")
    sync_todos(habitica_todos, dashboard_todos, user_id)

    print("Sync done todos")
    sync_todos(habitica_done_todos, dashboard_todos, user_id)

    print("Sync dailies")
    sync_dailies(habitica_dailies, dashboard_dailies, user_id)

    print("Sync habits")
    sync_habits(habitica_habits, dashboard_habits, user_id)


if __name__ == '__main__':
    sync()
