from datetime import date

from .schema import CodeWarsUserSchema, \
    CodeWarsUserStatisticSchema, LanguageInfoSchema, LanguageScoreSchema


def test_CodeWarsUserSchema_works():  # noqa
    user: CodeWarsUserSchema = CodeWarsUserSchema(
        **{"name": "Bilbo"}
    )

    assert user.name == "Bilbo"


def test_CodeWarsUserStatisticSchema_works():  # noqa
    user_statistic: CodeWarsUserStatisticSchema = CodeWarsUserStatisticSchema(
        **{"honor": 123,
           "leaderboard_position": 999,
           "kata_completed": 100,
           "last_update": date.today()
           }
    )

    assert user_statistic.honor == 123
    assert user_statistic.leaderboard_position == 999
    assert user_statistic.kata_completed == 100
    assert user_statistic.last_update == date.today()


def test_LanguageInfoSchema_works():  # noqa
    lang: LanguageInfoSchema = LanguageInfoSchema(
        **{"name": "c++"}
    )

    assert lang.name == "c++"


def test_LanguageScoreSchema_works():  # noqa
    lang_score: LanguageScoreSchema = LanguageScoreSchema(
        **{"score": 123,
           "rank": 999,
           "lang_id": 100,
           "last_update": date.today()
           }
    )

    assert lang_score.score == 123
    assert lang_score.rank == 999
    assert lang_score.lang_id == 100
    assert lang_score.last_update == date.today()
