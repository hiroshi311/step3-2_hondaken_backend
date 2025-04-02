from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from app.core.database import Base
from zoneinfo import ZoneInfo
from datetime import datetime

# get_jst_now 関数を定義
def get_jst_now():
    return datetime.now(ZoneInfo("Asia/Tokyo"))

class Reservation(Base):
    __tablename__ = "reservations"  # 複数形に修正！

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    dog_id = Column(Integer, ForeignKey("dogs.id"), nullable=False)

    check_in_time = Column(DateTime, nullable=False)
    check_out_time = Column(DateTime, nullable=False)
    status = Column(String(25), default="予約済み")

    created_at = Column(DateTime, default=get_jst_now)

    # 文字列でクラス名を指定して循環インポートを回避
    user = relationship("User", back_populates="reservations", lazy="joined")
    dog = relationship("Dog", back_populates="reservations", lazy="joined")  # 文字列指定
    location = relationship("Location", back_populates="reservations", lazy="joined")
