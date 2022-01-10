
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
        print(response.json())
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
        print(response.json())
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
        print(response.json())
        raise requests.HTTPError


def sync_todos(habitica_todos: list, dashboard_todos: list, user_id: int) -> None:
    for h_todo in habitica_todos:
        todo_exist = False
        for d_todo in dashboard_todos:
            if d_todo['habiticaID'] == h_todo.habiticaID:
                print("Todo already exist, check if need update")
                todo_exist = True
                if d_todo['priority'] == h_todo.priority \
                        and d_todo['text'] == h_todo.text:
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
    habitica_todos = habitica_client.get_todos()
    habitica_done_todos = habitica_client.get_done_todos()

    print("Sync todos")
    sync_todos(habitica_todos, dashboard_todos, user_id)

    print("Sync done todos")
    sync_todos(habitica_done_todos, dashboard_todos, user_id)


if __name__ == '__main__':
    sync()
