from datetime import datetime
from pprint import pprint

import requests
import json
from CodeWarsInterface import CodeWarsInterface


def date_get(url: str):
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


def date_post(url: str, data: json):
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


def sync() -> None:
    user_name = 'biniu'

    code_wars_client = CodeWarsInterface(user_name)

    users = date_get(url="http://127.0.0.1:8000/CodeWars/users")
    user_exist = list(filter(lambda user: user['name'] == user_name, users))

    if user_exist:
        print("User already exist")
        user_id = user_exist[0]['id']
    else:
        print("Creating user")
        data = date_post(url="http://127.0.0.1:8000/CodeWars/users", data={"name": "biniu"})
        user_id = data['user_id']

    data = {
      "honor": code_wars_client.get_user_honor(),
      "leaderboard_position": code_wars_client.get_leaderboard_position(),
      "kata_completed": code_wars_client.get_completed_kata(),
      "last_update": datetime.today().strftime('%Y-%m-%d')
    }

    date_post(
        url=f"http://127.0.0.1:8000/CodeWars/UserStatistics/{user_id}",
        data=data
    )

    pprint(date_get(f"http://127.0.0.1:8000/CodeWars/UserStatistics/{user_id}"))


if __name__ == '__main__':
    sync()
