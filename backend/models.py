from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Sprint(Base):
    __tablename__ = 'sprints'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<Sprint {self.name!r}>'