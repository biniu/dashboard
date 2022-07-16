from datetime import datetime

from fastapi import Depends
from requests import Session

from app.db import get_db
from app.routers.CodeWars.CodeWarsInterface import CodeWarsInterface
from app.routers.CodeWars.model import CodeWarsUser, \
    CodeWarsUserStatistic, LanguageInfo, LanguageScore
from app.routers.CodeWars.service import CodeWarsService


async def sync(db: Session = Depends(get_db)) -> None:
    user_name = 'biniu'

    code_wars_client = CodeWarsInterface(user_name)
    print("Sync get data")

    if await CodeWarsService.user_with_name_exist(user_name, db):
        print("User already exist")
        user_id = await CodeWarsService.get_user_id(user_name, db)
    else:
        print("Creating user")
        user_id = await CodeWarsService.create_user(
            user=CodeWarsUser(name=user_name),
            db=db)

    print(f"user_id {user_id}")

    await CodeWarsService.create_user_statistics(
        user_id=user_id,
        user_statistics=CodeWarsUserStatistic(
            honor=code_wars_client.get_user_honor(),
            leaderboard_position=code_wars_client.get_leaderboard_position(),
            kata_completed=code_wars_client.get_completed_kata(),
            last_update=datetime.today().strftime('%Y-%m-%d')
        ),
        db=db
    )

    languages = code_wars_client.get_language_list()
    create_languages = await CodeWarsService.get_language_infos(db)
    print(create_languages)

    for language in languages:
        print(language)
        if await CodeWarsService.lang_with_name_exist(language, db):
            lang_id = await CodeWarsService.get_lang_id(language, db)
        else:
            lang_id = await CodeWarsService.create_language_infos(
                language_info=LanguageInfo(name=language), db=db)

        print(f"lang_id {lang_id}")
        lang_stats = code_wars_client.get_language_statistics(language)

        await CodeWarsService.create_language_scores(
            user_id=user_id,
            language_score=LanguageScore(
                score=lang_stats['score'],
                rank=lang_stats['rank'],
                lang_id=lang_id,
                last_update=datetime.today().strftime('%Y-%m-%d')
            ),
            db=db
        )
