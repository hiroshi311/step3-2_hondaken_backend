from sqlalchemy import Column, Integer, String ,Float ,DateTime ,ForeignKey ,Boolean
from sqlalchemy.orm import declarative_base, relationship # ← ✅ここ修正！
from datetime import datetime
from app.models.reservation import Reservation  # Reservationをインポート
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, String
from app.core.database import Base



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

    user = relationship("User", back_populates="dogs", lazy="joined")
    reservations = relationship("Reservation", back_populates="dog", lazy="joined")  # Reservationとのリレーション追加