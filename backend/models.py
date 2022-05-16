from typing import Collection
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Boolean
from .database import Base


class Sprint(Base):
    __tablename__ = 'sprints'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Integer)

    def __init__(self, name, start_date, end_date, is_active):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active

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
    status = Column(String(15))

    def __init__(self, name, description, sprint, monitorer, epic, signaler, fibonacci_points, status):
        self.name = name
        self.description = description
        self.sprint = sprint
        self.monitorer = monitorer
        self.epic = epic
        self.signaler = signaler
        self.fibonacci_points = fibonacci_points
        self.status = status

    def __repr__(self):
        return f'<Task {self.name!r}>'

class SubTask(Base):
    __tablename__ = 'subtasks'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(Text())
    assigned_to = Column(Integer, ForeignKey('users.id'), nullable=True)



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

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    email = Column(String(50))
    password = Column(String(256)) # SHA256
    manager = Column(Boolean())

    def __init__(self, name, surname, email, password, manager=False):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.manager = manager

    def __repr__(self):
        return f'< User {self.email!r} >'