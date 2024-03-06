from datetime import datetime
from sqlalchemy import Column, DateTime, String, Integer
from .database import Base


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, default=datetime.now)
    question = Column(String)
    answer = Column(String)
