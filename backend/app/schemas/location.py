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
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
class Config:
    from_attributes = True
