from sqlalchemy import Column, String, INTEGER, DATE
from datetime import datetime
from base import Base


class Task(Base):
    __tablename__ = 'task'
    id = Column(INTEGER, primary_key=True)
    task = Column(String)
    deadline = Column(DATE, default=datetime.today())

    def __str__(self):
        return self.task
