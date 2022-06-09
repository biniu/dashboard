from datetime import datetime, date

from pydantic import BaseModel
from sqlalchemy import ForeignKey, Column, Integer, String, DATE
from sqlalchemy.orm import relationship

from app.database import Base


class CodeWarsUsers(Base):
    __tablename__ = "CodeWarsUsers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    def __str__(self):
        return f"ID {self.id} {self.name}"


class CodeWarsUserStatistics(Base):
    __tablename__ = "CodeWarsUserStatistics"

    id = Column(Integer, primary_key=True, index=True)
    honor = Column(Integer)
    leaderboard_position = Column(Integer)
    kata_completed = Column(Integer)
    last_update = Column(DATE, server_default=datetime.today().strftime('%Y-%m-%d'))

    user_id = Column(Integer, ForeignKey(CodeWarsUsers.id))
    user = relationship("CodeWarsUsers")

    def __str__(self):
        return f"ID {self.id} user [{self.user}] date {self.last_update} honor {self.honor}"


class LanguageInfos(Base):
    __tablename__ = "LanguageInfos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    def __str__(self):
        return f"ID {self.id} {self.name}"


class LanguageScores(Base):
    __tablename__ = "LanguageScores"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    rank = Column(Integer)
    last_update = Column(DATE, server_default=datetime.today().strftime('%Y-%m-%d'))

    user_id = Column(Integer, ForeignKey(CodeWarsUsers.id))
    user = relationship("CodeWarsUsers")

    lang_id = Column(Integer, ForeignKey(LanguageInfos.id))
    lang = relationship("LanguageInfos")


class CodeWarsUser(BaseModel):
    name: str


class CodeWarsUserStatistic(BaseModel):
    honor: int
    leaderboard_position: int
    kata_completed: int

    last_update: date


class LanguageInfo(BaseModel):
    name: str


class LanguageScore(BaseModel):
    score: int
    rank: int

    lang_id: int

    last_update: date
