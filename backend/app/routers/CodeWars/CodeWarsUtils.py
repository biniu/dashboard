from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.routers.CodeWars import CodeWarsModels
from app.routers.CodeWars.CodeWarsModels import CodeWarsUser, \
    CodeWarsUserStatistic, LanguageInfo, LanguageScore


def get_user_id(user: str, db: Session = Depends(get_db)) -> bool:
    return db.query(CodeWarsModels.CodeWarsUsers).filter(
        CodeWarsModels.CodeWarsUsers.name == user).first().id


def user_with_name_exist(user: str, db: Session = Depends(get_db)) -> bool:
    if db.query(CodeWarsModels.CodeWarsUsers).filter(
            CodeWarsModels.CodeWarsUsers.name == user).first():
        return True
    return False


def user_with_id_exist(user_id: int, db: Session = Depends(get_db)) -> bool:
    if db.query(CodeWarsModels.CodeWarsUsers).filter(
            CodeWarsModels.CodeWarsUsers.id == user_id).first():
        return True
    return False


def lang_with_name_exist(language_name: str,
                         db: Session = Depends(get_db)) -> bool:
    if db.query(CodeWarsModels.LanguageInfos).filter(
            CodeWarsModels.LanguageInfos.name == language_name).first():
        return True
    return False


def get_lang_id(language_name: str, db: Session = Depends(get_db)) -> bool:
    return db.query(CodeWarsModels.LanguageInfos).filter(
        CodeWarsModels.LanguageInfos.name == language_name).first().id


def get_users(db: Session = Depends(get_db)):
    return db.query(CodeWarsModels.CodeWarsUsers).all()


def create_user(user: CodeWarsUser, db: Session = Depends(get_db)):
    if user_with_name_exist(user.name, db):
        raise HTTPException(status_code=400, detail="User already exists")

    user_info_model = CodeWarsModels.CodeWarsUsers()
    user_info_model.name = user.name

    db.add(user_info_model)
    db.commit()

    created_user = db.query(CodeWarsModels.CodeWarsUsers). \
        filter(CodeWarsModels.CodeWarsUsers.name == user.name) \
        .first()

    print(created_user)

    return created_user.id


def get_user_statistics(user_id: int, db: Session = Depends(get_db)):
    if not user_with_id_exist(user_id, db):
        raise HTTPException(status_code=400,
                            detail=f"User with ID {user_id} not exist")

    user_statistics = db.query(CodeWarsModels.CodeWarsUserStatistics) \
        .filter(CodeWarsModels.CodeWarsUserStatistics.user_id == user_id)
    return user_statistics.all()


def create_user_statistics(user_id: int, user_statistics: CodeWarsUserStatistic,
                           db: Session = Depends(get_db)) -> None:
    print("create_user_statistics")
    if not user_with_id_exist(user_id, db):
        raise HTTPException(status_code=400,
                            detail=f"User with ID {user_id} not exist")

    if user_statistics.last_update:
        print("data from parm")
        statistic_date = user_statistics.last_update
    else:
        print("create new date")
        statistic_date = datetime.today().strftime('%Y-%m-%d')

    last_update = db.query(CodeWarsModels.CodeWarsUserStatistics) \
        .filter(
        CodeWarsModels.CodeWarsUserStatistics.last_update == statistic_date)

    if last_update.first():
        print(f"User statistic for {statistic_date} exist -> update exist one")
        user_statistics_model = last_update.first()
    else:
        print(
            f"User statistic for {statistic_date} not exist -> create new one")
        user_statistics_model = CodeWarsModels.CodeWarsUserStatistics()
    user_statistics_model.honor = user_statistics.honor
    user_statistics_model.leaderboard_position = user_statistics.leaderboard_position
    user_statistics_model.kata_completed = user_statistics.kata_completed
    user_statistics_model.user_id = user_id

    if user_statistics.last_update:
        user_statistics_model.last_update = statistic_date

    db.add(user_statistics_model)
    db.commit()


def get_language_infos(db: Session = Depends(get_db)):
    return db.query(CodeWarsModels.LanguageInfos).all()


def create_language_infos(language_info: LanguageInfo,
                          db: Session = Depends(get_db)):
    if db.query(CodeWarsModels.LanguageInfos).filter(
            CodeWarsModels.LanguageInfos.name == language_info.name).first():
        raise HTTPException(status_code=400,
                            detail=f"Language {language_info.name} already exists")

    language_info_model = CodeWarsModels.LanguageInfos()
    language_info_model.name = language_info.name

    db.add(language_info_model)
    db.commit()

    created_language = db.query(CodeWarsModels.LanguageInfos). \
        filter(CodeWarsModels.LanguageInfos.name == language_info.name) \
        .first()

    return created_language.id


def get_languages_scores(user_id: int, db: Session = Depends(get_db)):
    if not db.query(CodeWarsModels.CodeWarsUsers) \
            .filter(CodeWarsModels.CodeWarsUsers.id == user_id).first():
        raise HTTPException(status_code=400,
                            detail=f"User with ID {user_id} not exist")

    query = select(
        (CodeWarsModels.LanguageScores, CodeWarsModels.LanguageInfos.name),
    ).select_from(
        CodeWarsModels.LanguageScores
    ).where(
        CodeWarsModels.LanguageScores.lang_id == CodeWarsModels.LanguageInfos.id
    )

    result = engine.execute(query)
    out = []
    for row in result:
        out.append(dict(row))

    return out


async def get_language_scores(user_id: int, lang_id: int,
                              db: Session = Depends(get_db)):
    if not db.query(CodeWarsModels.CodeWarsUsers) \
            .filter(CodeWarsModels.CodeWarsUsers.id == user_id).first():
        raise HTTPException(status_code=400,
                            detail=f"User with ID {user_id} not exist")

    if not db.query(CodeWarsModels.LanguageInfos) \
            .filter(CodeWarsModels.LanguageInfos.id == lang_id).first():
        raise HTTPException(status_code=400,
                            detail=f"Lang with ID {lang_id} not exist")

    return db.query(CodeWarsModels.LanguageScores) \
        .filter(CodeWarsModels.LanguageScores.lang_id == lang_id) \
        .filter(CodeWarsModels.LanguageScores.user_id == user_id).all()


def create_language_scores(user_id: int, language_score: LanguageScore,
                           db: Session = Depends(get_db)):
    if not db.query(CodeWarsModels.CodeWarsUsers) \
            .filter(CodeWarsModels.CodeWarsUsers.id == user_id).first():
        raise HTTPException(status_code=400,
                            detail=f"User with ID {user_id} not exist")

    if not db.query(CodeWarsModels.LanguageInfos) \
            .filter(
        CodeWarsModels.LanguageInfos.id == language_score.lang_id).first():
        raise HTTPException(status_code=400,
                            detail=f"Lang with ID {language_score.lang_id} not exist")

    if language_score.last_update:
        print("data from parm")
        statistic_date = language_score.last_update
    else:
        print("create new date")
        statistic_date = datetime.today().strftime('%Y-%m-%d')

    last_update = db.query(CodeWarsModels.LanguageScores) \
        .filter(CodeWarsModels.LanguageScores.last_update == statistic_date) \
        .filter(CodeWarsModels.LanguageScores.lang_id == language_score.lang_id) \
        .filter(CodeWarsModels.LanguageScores.user_id == user_id)

    if last_update.first():
        print(
            f"Lang statistic for {statistic_date} {user_id} exist -> update exist one")
        language_score_model = last_update.first()
    else:
        print(
            f"Lang statistic for {statistic_date} {user_id} not exist -> create new one")
        language_score_model = CodeWarsModels.LanguageScores()

    language_score_model.score = language_score.score
    language_score_model.rank = language_score.rank
    language_score_model.user_id = user_id
    language_score_model.lang_id = language_score.lang_id

    if language_score.last_update:
        language_score_model.last_update = statistic_date

    db.add(language_score_model)
    db.commit()
