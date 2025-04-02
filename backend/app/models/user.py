from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from zoneinfo import ZoneInfo
from app.core.database import Base

# JSTの現在時刻を返す関数
def get_jst_now():
    return datetime.now(ZoneInfo("Asia/Tokyo"))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name_last = Column(String(30), nullable=False)
    name_first = Column(String(30), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    birthday = Column(DateTime, nullable=True)
    postal_code = Column(String(7))
    prefecture = Column(String(4))
    city = Column(String(50))
    address_line = Column(String(100))
    phone_number = Column(String(11))
    hashed_password = Column(String(255))
    gender = Column(String(10))
    google_id = Column(String(255), nullable=True)
    profile_image_url = Column(String(255), nullable=True)
    line_u_id = Column(String(64), nullable=True)

    created_at = Column(DateTime, default=get_jst_now)
    updated_at = Column(DateTime, default=get_jst_now, onupdate=get_jst_now)

    # 予約・ワンちゃんとのリレーション
    reservations = relationship("Reservation", back_populates="user", lazy="joined")
    dogs = relationship("Dog", back_populates="user", lazy="joined")


