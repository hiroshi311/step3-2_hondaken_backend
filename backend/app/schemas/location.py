from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LocationBase(BaseModel):
    name: str
    postal_code: str
    prefecture: str
    city: str
    address_line: str
    phone_number: str
    latitude: float
    longitude: float


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
class Config:
    from_attributes = True
