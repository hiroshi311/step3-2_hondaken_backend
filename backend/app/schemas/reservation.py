from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReservationBase(BaseModel):
    user_id: int
    location_id: int
    dog_id: int
    check_in_time: datetime
    check_out_time: datetime
    status: str = Field(default="予約済み")


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # SQLAlchemyモデルと連携できるようにする
