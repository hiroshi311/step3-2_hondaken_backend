from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base
from zoneinfo import ZoneInfo
from sqlalchemy.orm import relationship

# get_jst_now 関数を定義
def get_jst_now():
    return datetime.now(ZoneInfo("Asia/Tokyo"))

class QRCode(Base):
    __tablename__ = 'qr_codes'
    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"))
    qr_type = Column(String(25))  # 'checked-in' or 'checked-out'
    code = Column(String(255))
    created_at = Column(DateTime, default=get_jst_now)

    # Reservationとのリレーションを定義
    reservation = relationship("Reservation", back_populates="qr_code", lazy="joined")