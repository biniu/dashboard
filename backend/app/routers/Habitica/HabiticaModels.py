from sqlalchemy import ForeignKey, Column, Integer, String, DATE, Boolean, DATETIME
from sqlalchemy.orm import relationship

from datetime import datetime
from app.database import Base


class HabiticaUsers(Base):
    __tablename__ = "HabiticaUsers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    def __str__(self):
        return f"ID {self.id} {self.name}"


class HabiticaTodos(Base):
    __tablename__ = "HabiticaTodos"

    id = Column(Integer, primary_key=True, index=True)
    habiticaID = Column(String)

    createdAt = Column(DATETIME)
    completedAt = Column(DATETIME, nullable=True)
    completed = Column(Boolean)

    priority = Column(Integer)
    text = Column(String)

    user_id = Column(Integer, ForeignKey(HabiticaUsers.id))
    user = relationship("HabiticaUsers")

    def __str__(self):
        return f"Text {self.text} ID {self.id}"


class HabiticaHabits(Base):
    __tablename__ = "HabiticaHabits"

    id = Column(Integer, primary_key=True, index=True)
    habiticaID = Column(String)

    createdAt = Column(DATETIME)

    up = Column(Boolean)
    down = Column(Boolean)
    counterUp = Column(Integer)
    counterDown = Column(Integer)

    # TODO: change to enum after migrating to postgreSQL
    # tmp defs:
    # 1 -> daily
    # 2 -> weekly
    # 3 -> monthly
    frequency = Column(String)

    priority = Column(Integer)
    text = Column(String)

    user_id = Column(Integer, ForeignKey(HabiticaUsers.id))
    user = relationship("HabiticaUsers")

    history = relationship("HabiticaHabitHistory", back_populates="habit")


class HabiticaHabitHistory(Base):
    __tablename__ = "HabiticaHabitHistory"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DATE, server_default=datetime.today().strftime('%Y-%m-%d'))

    scoredUp = Column(Integer)
    scoredDown = Column(Integer)

    habit_id = Column(Integer, ForeignKey("HabiticaHabits.id"))
    habit = relationship("HabiticaHabits", back_populates="history")


class HabiticaDailies(Base):
    __tablename__ = "HabiticaDailies"

    id = Column(Integer, primary_key=True, index=True)
    habiticaID = Column(String)

    createdAt = Column(DATETIME)

    # TODO: change to enum after migrating to postgreSQL
    # tmp defs:
    # 1 -> daily
    # 2 -> weekly
    # 3 -> monthly
    # 4 -> yearly
    frequency = Column(String)
    everyX = Column(Integer)

    priority = Column(Integer)
    text = Column(String)

    completed = Column(Boolean)

    user_id = Column(Integer, ForeignKey(HabiticaUsers.id))
    user = relationship("HabiticaUsers")

    history = relationship("HabiticaDailiesHistory", back_populates="daily")


class HabiticaDailiesHistory(Base):
    __tablename__ = "HabiticaDailiesHistory"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DATE, server_default=datetime.today().strftime('%Y-%m-%d'))
    due = Column(Boolean)
    completed = Column(Boolean)

    daily_id = Column(Integer, ForeignKey("HabiticaDailies.id"))
    daily = relationship("HabiticaDailies", back_populates="history")
