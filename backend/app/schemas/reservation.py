from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# 🎯 予約作成リクエスト用：user_id / dog_id / check_in/out は送らせない
class ReservationCreate(BaseModel):
    location_id: int
    scheduled_start_time: datetime
    scheduled_end_time: datetime


class Reservation(BaseModel):
    id: int
    user_id: int
    dog_id: int
    location_id: int
    scheduled_start_time: datetime
    scheduled_end_time: datetime
    check_in_time: Optional[datetime]
    check_out_time: Optional[datetime]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True  # SQLAlchemyモデルと連携できるようにする

# 予約詳細取得用レスポンススキーマ
class ReservationDetail(BaseModel):
    user_last_name: str
    user_first_name: str
    location_name: str
    dog_name: str
    dog_breed: str
    dog_weight: float

    class Config:
        orm_mode = True