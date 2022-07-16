from typing import List

import pytest

from app.db import Session
from app.test.fixtures import app, session  # noqa
from .model import CodeWarsUser, LanguageInfo
from .schema import CodeWarsUserSchema, LanguageInfoSchema
from .service import CodeWarsService


@pytest.mark.asyncio
async def test_user_with_name_exist(session: Session):
    user_exist = "Bilbo"
    user_not_exist = "Sam"
    user: CodeWarsUserSchema = CodeWarsUserSchema(**{"name": user_exist})

    session.add(CodeWarsUser(**user.dict()))
    session.commit()

    assert await CodeWarsService.user_with_name_exist(user_exist, session)
    assert not await CodeWarsService.user_with_name_exist(user_not_exist,
                                                          session)


@pytest.mark.asyncio
async def test_user_with_id_exist(session: Session):
    user_exist = 1
    user_not_exist = 2
    user: CodeWarsUserSchema = CodeWarsUserSchema(**{"name": user_exist})

    session.add(CodeWarsUser(**user.dict()))
    session.commit()

    assert await CodeWarsService.user_with_id_exist(user_exist, session)
    assert not await CodeWarsService.user_with_id_exist(user_not_exist,
                                                        session)


@pytest.mark.asyncio
async def test_lang_with_name_exist(session: Session):
    lang_exist = "C++"
    lang_not_exist = "Python"
    lang: LanguageInfoSchema = LanguageInfoSchema(**{"name": lang_exist})

    session.add(LanguageInfo(**lang.dict()))
    session.commit()

    assert await CodeWarsService.lang_with_name_exist(lang_exist, session)
    assert not await CodeWarsService.lang_with_name_exist(lang_not_exist,
                                                          session)


@pytest.mark.asyncio
async def test_get_user_id(session: Session):
    user: CodeWarsUserSchema = CodeWarsUserSchema(**{"name": "Bilbo"})

    session.add(CodeWarsUser(**user.dict()))
    session.commit()

    results = await CodeWarsService.get_user_id(user.name, session)

    assert results == 1


@pytest.mark.asyncio
async def test_get_lang_id(session: Session):
    lang: LanguageInfoSchema = LanguageInfoSchema(**{"name": "Bilbo"})

    session.add(LanguageInfo(**lang.dict()))
    session.commit()

    results = await CodeWarsService.get_lang_id(lang.name, session)

    assert results == 1


@pytest.mark.asyncio
async def test_get_all_users(session: Session):
    user_1: CodeWarsUserSchema = CodeWarsUserSchema(**{"name": "Bilbo"})
    user_2: CodeWarsUserSchema = CodeWarsUserSchema(**{"name": "Sam"})

    session.add(CodeWarsUser(**user_1.dict()))
    session.add(CodeWarsUser(**user_2.dict()))
    session.commit()

    results: List[CodeWarsUserSchema] = await CodeWarsService.get_all_users(
        session)

    assert len(results) == 2
    assert user_1 in results and user_2 in results
