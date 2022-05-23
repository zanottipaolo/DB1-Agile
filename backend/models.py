from email.policy import default
from typing import Collection
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from flask_login import UserMixin


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
    status = Column(String(15))  # TODO, INPROGESS, DONE
    subtasks = relationship("SubTask")

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
    status = Column(String(15))  # TODO, INPROGESS, DONE
    task = Column(Integer, ForeignKey('tasks.id'))
    #task = relationship("Task", back_populates="subtasks")

    def __init__(self, name, description, task, assigned_to=None):
        self.name = name
        self.description = description
        self.assigned_to = assigned_to
        self.task = task
        self.status = 'TODO'

    def __repr__(self):
        return f'< Subtask {self.name!r} >'


class Epic(Base):
    __tablename__ = 'epics'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(Text())
    color = Column(Text)

    def __init__(self, name, description, color):
        self.name = name
        self.description = description
        self.color = color

    def __repr__(self):
        return f'< Epic {self.name!r} >'


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    email = Column(String(50))
    password = Column(String(256))  # SHA256
    manager = Column(Boolean(), default=0)
    url_profile_image = Column(String(50))

    def __init__(self, name, surname, email, password, manager):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.manager = manager

    def __repr__(self):
        return f'< User {self.email!r} >'


class Work(Base):
    __tablename__ = 'works'
    id = Column(Integer, primary_key=True)
    timeStamp_start = Column(String(50))
    duration = Column(Integer)
    developer = Column(Integer, ForeignKey('users.id'), nullable=True)
    subtask = Column(Integer, ForeignKey('subtasks.id'))

    def __init__(self, timeStamp_start, duration=duration, developer=developer, subtask=subtask):
        self.timeStamp_start = timeStamp_start
        self.duration = duration
        self.developer = developer
        self.subtask = subtask

    def __repr__(self):
        return f'< Work {self.name!r} >'
