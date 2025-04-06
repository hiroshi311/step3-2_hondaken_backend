from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.dog import Dog
from app.models.user import User
from app.schemas.dog import DogCreate, DogUpdate


def get_dogs_by_user(db: Session, user_id: int):
    return db.query(Dog).filter(Dog.user_id == user_id).all()


def get_dog(db: Session, dog_id: int):
    return db.query(Dog).filter(Dog.id == dog_id).first()


def create_dog(db: Session, dog: DogCreate, owner: User):
    try:
        db_dog = Dog(**dog.dict(), user_id=owner.id)
        db.add(db_dog)
        db.commit()
        db.refresh(db_dog)
        return db_dog
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create dog")



def update_dog(db: Session, dog_id: int, dog: DogUpdate):
    db_dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if db_dog:
        for key, value in dog.dict(exclude_unset=True).items():
            setattr(db_dog, key, value)
        db.commit()
        db.refresh(db_dog)
    return db_dog