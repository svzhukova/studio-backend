from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    instructor = Column(String)
    datetime = Column(DateTime)
