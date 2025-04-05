from sqlalchemy.orm import Session
from app.models.qrcode import QRCode
from app.schemas.qrcode import QRCodeCreate

def create_qrcode(db: Session, qr: QRCodeCreate):
    db_qr = QRCode(**qr.dict())
    db.add(db_qr)
    db.commit()
    db.refresh(db_qr)
    return db_qr

def get_qrcode_by_reservation_and_type(db: Session, reservation_id: int, qr_type: str):
    return db.query(QRCode).filter(
        QRCode.reservation_id == reservation_id,
        QRCode.qr_type == qr_type
    ).first()
