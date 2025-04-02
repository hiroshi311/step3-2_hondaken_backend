# app/api/dog.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.dog import Dog, DogCreate, DogUpdate
from app.core.database import get_db
from app.crud import dog as crud_dog

router = APIRouter(prefix="/dogs", tags=["dogs"])

@router.get("/user/{user_id}", response_model=List[Dog])
def get_user_dogs(user_id: int, db: Session = Depends(get_db)):
    return crud_dog.get_dogs_by_user(db, user_id)

@router.get("/{dog_id}", response_model=Dog)
def get_dog(dog_id: int, db: Session = Depends(get_db)):
    db_dog = crud_dog.get_dog(db, dog_id)
    if db_dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    return db_dog

@router.post("/", response_model=Dog)
def create_dog(dog: DogCreate, db: Session = Depends(get_db)):
    return crud_dog.create_dog(db, dog)

@router.put("/{dog_id}", response_model=Dog)
def update_dog(dog_id: int, dog: DogUpdate, db: Session = Depends(get_db)):
    db_dog = crud_dog.update_dog(db, dog_id, dog)
    if db_dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    return db_dog