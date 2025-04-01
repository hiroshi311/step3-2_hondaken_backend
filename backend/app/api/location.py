# app/api/location.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.location import Location as LocationSchema
from app.models.location import Location
from app.core.database import get_db
from app.crud import location as crud

router = APIRouter(prefix="/locations", tags=["locations"])

@router.get("/", response_model=List[LocationSchema])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_locations(db, skip=skip, limit=limit)

#1店舗に限ったGET必要
#@router.get("/", response_model=List[LocationSchema])
#def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    return crud.get_locations(db, skip=skip, limit=limit)