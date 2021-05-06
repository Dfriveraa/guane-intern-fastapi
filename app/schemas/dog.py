from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.schemas.user import UserBase


class DogBase(BaseModel):
    name: str
    picture: str

    class Config:
        orm_mode = True


class DogCreate(DogBase):
    publisher_id: int


class DogInfo(DogBase):
    is_adopted: bool
    created_at: Optional[datetime]
    publisher: Optional[UserBase] = None
    adopter: Optional[UserBase] = None


class ListDogs(BaseModel):
    offset: int
    limit: int
    total: int
    dogs: List[DogInfo]


class DogUpdateIn(BaseModel):
    adopter_id: Optional[int]
    is_adopted: bool

    class Config:
        orm_mode = True
