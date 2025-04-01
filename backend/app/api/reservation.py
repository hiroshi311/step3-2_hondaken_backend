from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.reservation import Reservation, ReservationCreate
from app.crud import reservation as crud
from app.core.database import SessionLocal

router = APIRouter(prefix="/reservations", tags=["reservations"])


# DBセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 予約一覧を取得
@router.get("/", response_model=List[Reservation])
def read_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_reservations(db, skip=skip, limit=limit)


# 単一予約を取得
@router.get("/{reservation_id}", response_model=Reservation)
def read_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = crud.get_reservation_by_id(db, reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation


# 予約作成
@router.post("/", response_model=Reservation)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    return crud.create_reservation(db, reservation)
