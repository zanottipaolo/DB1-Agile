from typing import Collection
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from .database import Base


class Sprint(Base):
    __tablename__ = 'sprints'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Integer)

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
    monitorer = Column(Integer)  # diventa chiave esterna
    epic = Column(Integer, ForeignKey('epics.id'), nullable=True)
    signaler = Column(Integer)  # diventa chiave esterna
    fibonacci_points = Column(Integer)

    def __init__(self, name, description, sprint, monitorer, epic, signaler, fibonacci_points):
        self.name = name
        self.description = description
        self.sprint = sprint
        self.monitorer = monitorer
        self.epic = epic
        self.signaler = signaler
        self.fibonacci_points = fibonacci_points

    def __repr__(self):
        return f'<Task {self.name!r}>'


class Epic(Base):
    __tablename__ = 'epics'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(Text())

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'< Epic {self.name!r} >'
