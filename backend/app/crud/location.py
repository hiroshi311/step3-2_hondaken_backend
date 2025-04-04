from sqlalchemy.orm import Session
from app.models.location import Location as LocationModel
from app.schemas.location import LocationCreate

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LocationModel).offset(skip).limit(limit).all()

def get_location_by_id(db: Session, location_id: int):
    return db.query(LocationModel).filter(LocationModel.id == location_id).first()