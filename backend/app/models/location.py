from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    postal_code = Column(String(7), nullable=True)
    prefecture = Column(String(4), nullable=True)
    city = Column(String(50), nullable=True)
    address_line = Column(String(255), nullable=True)
    phone_number = Column(String(15), nullable=True)
    latitude = Column(Float, nullable=True)    # MySQLのdouble対応
    longitude = Column(Float, nullable=True)   # MySQLのdouble対応

    # Reservationとのリレーションを定義
    reservations = relationship("Reservation", back_populates="location", lazy="joined")

