from typing import Collection
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from .database import Base

class Sprint(Base):
    __tablename__ = 'sprints'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Sprint {self.name!r}>'

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(Text())
    sprint = Column(Integer, ForeignKey('sprints.id'), nullable=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Task {self.name!r}>'
