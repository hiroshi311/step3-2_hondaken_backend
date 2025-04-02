from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

from app.core.database import Base

JST = pytz.timezone("Asia/Tokyo")

def get_jst_now():
    return datetime.now(JST)

class Reservation(Base):
    __tablename__ = "reservations"  # ← 複数形に修正！

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    dog_id = Column(Integer, ForeignKey("dogs.id"), nullable=False)

    check_in_time = Column(DateTime, nullable=False)
    check_out_time = Column(DateTime, nullable=False)
    status = Column(String(25), default="予約済み")

    created_at = Column(DateTime, default=get_jst_now)

    # 逆参照が必要なら User / Location / Dog 側でも back_populates を定義
    user = relationship("User", back_populates="reservations", lazy="joined")
    location = relationship("Location", back_populates="reservations", lazy="joined")
    dog = relationship("Dog", back_populates="reservations", lazy="joined")
