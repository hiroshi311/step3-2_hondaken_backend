from sqlalchemy import Column, Integer, String ,Float ,DateTime ,ForeignKey ,Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime


Base = declarative_base()

class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(String(10), nullable=True)
    breed = Column(String(50), nullable=True)
    birthday = Column(DateTime)
    weight = Column(Float, nullable=True) 
    is_vaccinated = Column(Boolean, nullable=False, default=False)
    is_neutered = Column(Boolean, nullable=False, default=False)