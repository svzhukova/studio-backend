from sqlalchemy import Column, Integer, String, Float
from database import Base

class Abonement(Base):
    __tablename__ = "abonements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    duration_days = Column(Integer)
