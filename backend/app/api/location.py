# app/api/location.py

from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/{location_id}", response_model=LocationSchema)
def read_location(location_id: int, db: Session = Depends(get_db)):
    location = crud.get_location_by_id(db, location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location