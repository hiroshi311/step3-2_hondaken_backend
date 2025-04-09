# app/api/location.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.location import Location as LocationSchema
from app.models.location import Location
from app.core.database import get_db
from app.crud import location as crud
from dotenv import load_dotenv
import os

load_dotenv()

AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
AZURE_BLOB_CONTAINER_NAME = os.getenv("AZURE_BLOB_CONTAINER_NAME")
AZURE_BLOB_PATH = os.getenv("AZURE_BLOB_PATH", "")
AZURE_BLOB_BASE_URL = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_BLOB_CONTAINER_NAME}/{AZURE_BLOB_PATH}"


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

@router.get("/{location_id}/image")
def get_location_image_url(location_id: int, db: Session = Depends(get_db)):
    location = crud.get_location_by_id(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    image_filename = f"{location_id}.jpg"
    image_url = AZURE_BLOB_BASE_URL + image_filename
    return {"image_url": image_url}
