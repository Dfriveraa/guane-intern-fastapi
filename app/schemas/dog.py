from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.user import UserBase


class DogBase(BaseModel):
    name: str
    picture: str
    is_adopted: bool
    created_date: datetime

    class Config:
        orm_mode = True


class ListDogs(BaseModel):
    offset: int
    limit: int
    total: int
    dogs: List[DogBase]


class DogUpdateIn(BaseModel):
    is_adopted: bool
    adopter_id: int

    class Config:
        orm_mode = True
