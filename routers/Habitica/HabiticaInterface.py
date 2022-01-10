import configparser as configparser
from pathlib import Path

import requests

from pprint import pprint as pp
from dataclasses import dataclass
from datetime import date


@dataclass
class HabiticaTodo:
    habiticaID: str
    createdAt: date
    completedAt: date
    completed: bool
    priority: int
    text: str


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
            # self.logger.error("Request failed!")
            # self.logger.error(response.status_code)
            # self.logger.error(response.reason)
            # self.logger.error(response.json())
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



if __name__ == "__main__":
    print("Main")
    habitica_client = HabiticaInterface()

    pp(habitica_client.get_todos())
    pp(habitica_client.get_done_todos())
