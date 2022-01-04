import requests


class CodeWarsInterface():

    def __init__(self, user_name) -> None:
        self._user_name = user_name
        self._user_data = ""
        self._date_request(url='http://localhost:3001/codeWarsUser')
        # self._date_request(url=f'https://www.codewars.com/api/v1/users/{self._user_name}')

    def _date_request(self, url: str) -> None:
        with requests.Session() as session:
            session = requests.Session()
            response = session.get(url)

        if response.status_code == 200:
            self._user_data = response.json()
        else:
            raise requests.HTTPError

    def get_user_name(self) -> str:
        return self._user_data['username']

    def get_user_honor(self) -> int:
        return int(self._user_data['honor'])

    def get_leaderboard_position(self) -> int:
        return int(self._user_data['leaderboardPosition'])

    def get_completed_kata(self) -> int:
        return int(self._user_data['codeChallenges']['totalCompleted'])

    def get_language_list(self) -> list:
        return list(self._user_data['ranks']['languages'])

    def get_language_statistics(self, language: str) -> dict:
        return dict(self._user_data['ranks']['languages'][language])

    def get_overall_statistics(self) -> dict:
        return dict(self._user_data['ranks']['overall'])


if __name__ == "__main__":
    print("Main")
    code_wars_client = CodeWarsInterface('biniu')

    print(code_wars_client.get_user_name())
    print(code_wars_client.get_user_honor())
    print(code_wars_client.get_leaderboard_position())
    print(code_wars_client.get_completed_kata())
    print(code_wars_client.get_language_list())
    print(code_wars_client.get_language_statistics('python'))
    print(code_wars_client.get_overall_statistics())
