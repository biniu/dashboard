import configparser as configparser
from pathlib import Path

import requests

from pprint import pprint as pp, pprint
from dataclasses import dataclass
from datetime import date, datetime

from typing import List
from dataclasses_json import dataclass_json



@dataclass
class HabiticaTodo:
    habiticaID: str
    createdAt: date
    completedAt: date
    completed: bool
    priority: int
    text: str


@dataclass_json
@dataclass
class HabiticaDailyHistoryEntry:
    date: date
    due: bool
    completed: bool


@dataclass_json
@dataclass
class HabiticaDaily:
    habiticaID: str
    createdAt: datetime
    frequency: str
    everyX: int
    priority: int
    text: str
    completed: bool
    isDue: bool
    history: List[HabiticaDailyHistoryEntry]


@dataclass_json
@dataclass
class HabiticaHabitHistoryEntry:
    date: date
    scoredUp: int
    scoredDown: int


@dataclass_json
@dataclass
class HabiticaHabit:
    habiticaID: str
    createdAt: datetime

    up: bool
    down: bool
    counterUp: int
    counterDown: int
    frequency: str
    priority: int
    text: str

    history: List[HabiticaHabitHistoryEntry]


class HabiticaInterface:

    def __init__(self) -> None:

        config = configparser.ConfigParser()
        config.readfp(open(f"{Path.home()}/.config/dashboard_config/config.cfg"))
        self._USER_ID = config.get('Habitica', 'USER_ID')
        self._TOKEN = config.get('Habitica', 'USER_KEY')

    def _date_request(self, url):
        with requests.Session() as session:
            session = requests.Session()
            session.auth = (self._USER_ID, self._TOKEN)
            session.headers.update({"x-api-user": self._USER_ID, "x-api-key": self._TOKEN}),

            response = session.get(url)

        # self.logger.debug(response.status_code)
        # self.logger.debug(response.reason)
        # self.logger.debug(response.json())
        #
        # pp(response.json())

        if response.status_code == 200:
            return response.json()
        else:
            print("Request failed!")
            print(response.status_code)
            print(response.reason)
            print(response.json())
            raise requests.HTTPError

    @staticmethod
    def _map_habitica_priority(habitica_priority):
        if habitica_priority == 0.1:  # trivial
            return 4
        elif habitica_priority == 1:  # easy
            return 3
        elif habitica_priority == 1.5:  # medium
            return 2
        elif habitica_priority == 2:  # hard
            return 1

        return 2

    def get_todos(self):

        out = []
        todos = self._date_request(
            # url="http://localhost:3001/habiticaTodos"
            url="https://habitica.com/api/v3/tasks/user?type=todos"
        )

        for todo in todos['data']:
            todo_model = HabiticaTodo(
                habiticaID=todo['id'],
                createdAt=todo['createdAt'],
                completedAt=None,
                completed=False,
                priority=self._map_habitica_priority(todo['priority']),
                text=todo['text']
            )

            out.append(todo_model)

        return out

    def get_done_todos(self):

        out = []
        todos = self._date_request(
            url="https://habitica.com/api/v3/tasks/user?type=completedTodos"
        )

        for todo in todos['data']:
            todo_model = HabiticaTodo(
                habiticaID=todo['id'],
                createdAt=todo['createdAt'],
                completedAt=todo['dateCompleted'],
                completed=True,
                priority=self._map_habitica_priority(todo['priority']),
                text=todo['text']
            )

            out.append(todo_model)

        return out

    def get_dailies(self):
        out = []
        dailies = self._date_request(
            # url="http://localhost:3001/habiticaDailies"
            url="https://habitica.com/api/v3/tasks/user?type=dailys"
        )

        for daily in dailies['data']:
            daily_history = []
            for elem in daily['history']:
                history_model = HabiticaDailyHistoryEntry(
                    date=elem['date'],
                    due=elem['isDue'],
                    completed=elem['completed']
                )
                daily_history.append(history_model)
            daily_model = HabiticaDaily(
                habiticaID=daily['id'],
                createdAt=daily['createdAt'],
                frequency=daily['frequency'],
                everyX=daily['everyX'],
                priority=self._map_habitica_priority(daily['priority']),
                text=daily['text'],
                completed=daily['completed'],
                isDue=daily['isDue'],
                history=daily_history
            )

            out.append(daily_model)
        return out

    def get_habits(self):
        out = []
        habits = self._date_request(
            # url="http://localhost:3001/habiticaHabits"
            url="https://habitica.com/api/v3/tasks/user?type=habits"
        )
        for habit in habits['data']:
            habit_history = []
            for elem in habit['history']:
                history_model = HabiticaHabitHistoryEntry(
                    date=elem['date'],
                    scoredUp=elem['scoredUp'],
                    scoredDown=elem['scoredDown']
                )
                habit_history.append(history_model)

            habit_model = HabiticaHabit(
                habiticaID=habit['id'],
                createdAt=habit['createdAt'],
                frequency=habit['frequency'],
                priority=self._map_habitica_priority(habit['priority']),
                text=habit['text'],
                up=habit['up'],
                down=habit['down'],
                counterUp=habit['counterUp'],
                counterDown=habit['counterDown'],
                history=habit_history
            )

            out.append(habit_model)
        return out


if __name__ == "__main__":
    print("Main")
    habitica_client = HabiticaInterface()

    # pp(habitica_client.get_todos())
    # pp(habitica_client.get_done_todos())

    pprint(habitica_client.get_habits())
