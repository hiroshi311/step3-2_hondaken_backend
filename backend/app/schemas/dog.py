from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DogBase(BaseModel):
    name: str
    type: Optional[str] = None
    breed: Optional[str] = None
    birthday: Optional[datetime] = None
    weight: Optional[float] = None
    is_vaccinated: bool
    is_neutered: bool


class DogCreate(DogBase):
    pass

class DogUpdate(DogBase):
    pass

# レスポンス時：user_id を含めてもOK
class Dog(DogBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True