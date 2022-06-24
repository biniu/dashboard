from datetime import date

from pydantic import BaseModel


class CodeWarsUserSchema(BaseModel):
    name: str


class CodeWarsUserStatisticSchema(BaseModel):
    honor: int
    leaderboard_position: int
    kata_completed: int

    last_update: date


class LanguageInfoSchema(BaseModel):
    name: str


class LanguageScoreSchema(BaseModel):
    score: int
    rank: int

    lang_id: int

    last_update: date
