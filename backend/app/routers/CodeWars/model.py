from datetime import datetime

from sqlalchemy import ForeignKey, Column, Integer, String, DATE
from sqlalchemy.orm import relationship

from app.db import Base


class CodeWarsUser(Base):
    __tablename__ = "CodeWarsUser"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    def __str__(self):
        return f"ID {self.id} {self.name}"


class CodeWarsUserStatistic(Base):
    __tablename__ = "CodeWarsUserStatistic"

    id = Column(Integer, primary_key=True, index=True)
    honor = Column(Integer)
    leaderboard_position = Column(Integer)
    kata_completed = Column(Integer)
    last_update = Column(DATE,
                         server_default=datetime.today().strftime('%Y-%m-%d'))

    user_id = Column(Integer, ForeignKey(CodeWarsUser.id))
    user = relationship("CodeWarsUser")

    def __str__(self):
        return f"ID {self.id} user [{self.user}] date {self.last_update} honor {self.honor}"


class LanguageInfo(Base):
    __tablename__ = "LanguageInfo"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    def __str__(self):
        return f"ID {self.id} {self.name}"


class LanguageScore(Base):
    __tablename__ = "LanguageScore"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    rank = Column(Integer)
    last_update = Column(DATE,
                         server_default=datetime.today().strftime('%Y-%m-%d'))

    user_id = Column(Integer, ForeignKey(CodeWarsUser.id))
    user = relationship("CodeWarsUser")

    lang_id = Column(Integer, ForeignKey(LanguageInfo.id))
    lang = relationship("LanguageInfo")
