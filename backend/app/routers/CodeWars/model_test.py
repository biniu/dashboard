from datetime import date

from pytest import fixture

from app.db import Session
from app.test.fixtures import app, session  # noqa
from .model import CodeWarsUser, CodeWarsUserStatistic, LanguageInfo, \
    LanguageScore
from .schema import CodeWarsUserSchema, CodeWarsUserStatisticSchema, \
    LanguageInfoSchema, LanguageScoreSchema


@fixture
def code_wars_user() -> CodeWarsUserSchema:
    code_wars_user = CodeWarsUserSchema(name="Frodo")
    return CodeWarsUser(**code_wars_user.dict())


def test_CodeWarsUser_create(code_wars_user: CodeWarsUserSchema): # noqa
    assert code_wars_user


def test_CodeWarsUser_retrieve(code_wars_user: CodeWarsUser, # noqa
                               session: Session):
    session.add(code_wars_user)
    session.commit()
    s = session.query(CodeWarsUser).first()
    assert s.__dict__ == code_wars_user.__dict__


@fixture
def code_wars_user_statistic() -> CodeWarsUserStatisticSchema:
    code_wars_user_statistic = CodeWarsUserStatisticSchema(honor=123,
                                                           leaderboard_position=123,
                                                           kata_completed=10,
                                                           last_update=date.today())
    return CodeWarsUserStatistic(**code_wars_user_statistic.dict())


def test_CodeWarsUserStatistic_create( # noqa
        code_wars_user_statistic: CodeWarsUserStatisticSchema):
    assert code_wars_user_statistic


def test_CodeWarsUserStatistic_retrieve( # noqa
        code_wars_user_statistic: CodeWarsUserStatistic,
        session: Session):
    session.add(code_wars_user_statistic)
    session.commit()
    s = session.query(CodeWarsUserStatistic).first()
    assert s.__dict__ == code_wars_user_statistic.__dict__


@fixture
def language_info() -> LanguageInfoSchema:
    language_info = LanguageInfoSchema(name="Python")
    return LanguageInfo(**language_info.dict())


def test_LanguageInfo_create(language_info: LanguageInfoSchema): # noqa
    assert language_info


def test_LanguageInfo_retrieve(language_info: LanguageInfo, # noqa
                               session: Session):
    session.add(language_info)
    session.commit()
    s = session.query(LanguageInfo).first()
    assert s.__dict__ == language_info.__dict__


@fixture
def language_score() -> LanguageScoreSchema:
    language_score = LanguageScoreSchema(
        score=123,
        rank=1,
        lang_id=1,
        last_update=date.today(),
    )
    return LanguageScore(**language_score.dict())


def test_LanguageScore_create(language_score: LanguageScoreSchema): # noqa
    assert language_score


def test_LanguageScore_retrieve(language_score: LanguageScore, # noqa
                                session: Session):
    session.add(language_score)
    session.commit()
    s = session.query(LanguageScore).first()
    assert s.__dict__ == language_score.__dict__
