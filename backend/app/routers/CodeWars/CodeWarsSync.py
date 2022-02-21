from datetime import datetime
from pprint import pprint

import requests
import json
from CodeWarsInterface import CodeWarsInterface


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


def sync() -> None:
    user_name = 'biniu'

    code_wars_client = CodeWarsInterface(user_name)

    users = data_get(url="http://127.0.0.1:8000/CodeWars/users")
    user_exist = list(filter(lambda user: user['name'] == user_name, users))

    if user_exist:
        print("User already exist")
        user_id = user_exist[0]['id']
    else:
        print("Creating user")
        data = data_post(url="http://127.0.0.1:8000/CodeWars/users", data={"name": user_name})
        user_id = data['user_id']


    print(f"user_id {user_id}")

    data = {
      "honor": code_wars_client.get_user_honor(),
      "leaderboard_position": code_wars_client.get_leaderboard_position(),
      "kata_completed": code_wars_client.get_completed_kata(),
      "last_update": datetime.today().strftime('%Y-%m-%d')
    }

    data_post(
        url=f"http://127.0.0.1:8000/CodeWars/UserStatistics/{user_id}",
        data=data
    )

    pprint(data_get(f"http://127.0.0.1:8000/CodeWars/UserStatistics/{user_id}"))

    languages = code_wars_client.get_language_list()
    create_languages = data_get(url="http://127.0.0.1:8000/CodeWars/LanguageInfos")
    print(create_languages)

    for language in languages:
        print(language)
        lang_exist = list(filter(lambda lang: lang['name'] == language, create_languages))
        if lang_exist:
            lang_id = lang_exist[0]['id']
        else:
            data = data_post(
                url="http://127.0.0.1:8000/CodeWars/LanguageInfos",
                data={"name": language}
            )
            lang_id = data['id']

        print(f"lang_id {lang_id}")
        lang_stats = code_wars_client.get_language_statistics(language)
        out = data_post(
            url=f"http://127.0.0.1:8000/CodeWars/LanguageScores/{user_id}",
            data={
                "score": lang_stats['score'],
                "rank": lang_stats['rank'],
                "lang_id": lang_id,
                "last_update": datetime.today().strftime('%Y-%m-%d')
            }
        )

        print(out)

    # pprint(data_get(url="http://127.0.0.1:8000/CodeWars/LanguageInfos"))


if __name__ == '__main__':
    sync()
