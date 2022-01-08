from sqlalchemy import ForeignKey, Column, Integer, String, DATE, Boolean, DATETIME
from sqlalchemy.orm import relationship

from datetime import datetime
from database import Base


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

    # createdAt = Column(DATE, server_default=datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    createdAt = Column(DATETIME)
    completedAt = Column(DATETIME, nullable=True)
    completed = Column(Boolean)

    priority = Column(Integer)
    text = Column(String)

    # tags = models.TextField() # TODO
    # reminders = # TODO

    user_id = Column(Integer, ForeignKey(HabiticaUsers.id))
    user = relationship("HabiticaUsers")

    def __str__(self):
        return f"Text {self.text} ID {self.id}"
