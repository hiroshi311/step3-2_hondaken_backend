from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.qrcode_generator import generate_qr_with_logo
from app.schemas.qrcode import QRCodeResponse, QRCodeCreate
from app.crud import qrcode as crud_qr
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/qr", tags=["QR"])

QR_BASE_URL = os.getenv("QR_BASE_URL")

@router.get("/generate", response_model=QRCodeResponse)
def generate_qrcode(reservation_id: int = Query(...), qr_type: str = Query(...), db: Session = Depends(get_db)):
    url = f"{QR_BASE_URL}/qr/update?reservation_id={reservation_id}&type={qr_type}"
    qr_image = generate_qr_with_logo(url)

    if not qr_image:
        raise HTTPException(status_code=500, detail="QRコード生成に失敗しました")

    existing = crud_qr.get_qrcode_by_reservation_and_type(db, reservation_id, qr_type)
    if existing:
        return existing

    qr_data = QRCodeCreate(reservation_id=reservation_id, qr_type=qr_type, code=qr_image)
    new_qr = crud_qr.create_qrcode(db, qr=qr_data)
    return new_qr