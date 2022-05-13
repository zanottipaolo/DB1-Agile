from sqlalchemy import Column, Integer, String, Date, null
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