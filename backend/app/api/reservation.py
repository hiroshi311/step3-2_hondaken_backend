from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from zoneinfo import ZoneInfo
from datetime import datetime
from fastapi import Query
from app.schemas.reservation import Reservation as ReservationSchema, ReservationCreate, ReservationDetail
from app.models.reservation import Reservation as ReservationModel
from app.crud import reservation as crud
from app.core.database import SessionLocal
from app.api.auth import get_current_user  # 🔑 JWTから現在のユーザーを取得
from app.models.user import User  # 🔑 User型アノテーションのため

router = APIRouter(prefix="/reservations", tags=["reservations"])


# DBセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_jst_now():
    return datetime.now(ZoneInfo("Asia/Tokyo"))


# 予約一覧を取得
@router.get("/", response_model=List[ReservationSchema])
def read_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_reservations(db, skip=skip, limit=limit)


# 🔁 ログインユーザーの未来予約一覧を取得
@router.get("/upcoming", response_model=List[ReservationSchema])
def get_upcoming_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    now = get_jst_now()
    return crud.get_upcoming_reservations(db, user_id=current_user.id, from_time=now)


# 単一予約を取得
@router.get("/{reservation_id}", response_model=ReservationSchema)
def read_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = crud.get_reservation_by_id(db, reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation


# 予約作成
@router.post("/", response_model=ReservationSchema)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    return crud.create_reservation(db, reservation)

# 🔁 ログインユーザーの予約作成
@router.post("/me", response_model=ReservationSchema)
def create_reservation_with_user(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← JWTログイン済みのユーザー情報
):
    return crud.create_reservation_with_user(db, reservation, current_user)

# 🔐 ログインユーザーの未来予約一覧
@router.get("/me/upcoming", response_model=List[ReservationSchema])
def get_my_upcoming_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    now = get_jst_now()
    return crud.get_upcoming_reservations(
        db=db,
        user_id=current_user.id,
        from_time=now
    )

@router.get("/reservations/{reservation_id}/detail", response_model=ReservationDetail)
def get_reservation_detail(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()

    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    return ReservationDetail(
        user_last_name=reservation.user.name_last,
        user_first_name=reservation.user.name_first,
        location_name=reservation.location.name,
        dog_name=reservation.dog.name,
        dog_breed=reservation.dog.breed,
        dog_weight=reservation.dog.weight
    )