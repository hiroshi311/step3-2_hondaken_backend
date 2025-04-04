from pydantic import BaseModel, Field
from datetime import datetime



class QRCodeBase(BaseModel):
    reservation_id: int
    qr_type: str


class QRCodeCreate(QRCodeBase):
    code: str


class QRCodeResponse(QRCodeBase):
    id: int
    code: str
    created_at: datetime

    class Config:
        orm_mode = True  # SQLAlchemyモデルと連携できるようにする