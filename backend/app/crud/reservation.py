from sqlalchemy.orm import Session
from fastapi import HTTPException  # ←追加！
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from datetime import datetime

# 外部モデルをインポート
from app.models.user import User
from app.models.dog import Dog
from app.models.location import Location


# 予約作成（user_id, dog_id, location_id の存在チェックあり）
def create_reservation(db: Session, reservation: ReservationCreate) -> Reservation:
    # user_id の存在確認
    user = db.query(User).filter(User.id == reservation.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    # dog_id の存在確認
    dog = db.query(Dog).filter(Dog.id == reservation.dog_id).first()
    if not dog:
        raise HTTPException(status_code=400, detail="Invalid dog_id")

    # location_id の存在確認
    location = db.query(Location).filter(Location.id == reservation.location_id).first()
    if not location:
        raise HTTPException(status_code=400, detail="Invalid location_id")

    db_reservation = Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

# 予約一覧取得
def get_reservations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reservation).offset(skip).limit(limit).all()


# 単一予約取得（ID指定）
def get_reservation_by_id(db: Session, reservation_id: int):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()


#未来予約一覧を取得
def get_upcoming_reservations(db: Session, user_id: int, from_time: datetime):
    return db.query(Reservation).filter(
        Reservation.user_id == user_id,
        Reservation.check_in_time >= from_time
    ).all()
