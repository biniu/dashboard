from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, func, DATE
from sqlalchemy.orm import relationship

from datetime import datetime

# import from SQLAlchemy setup file 
from database import Base


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
