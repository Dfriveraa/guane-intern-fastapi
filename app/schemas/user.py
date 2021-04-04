from pydantic import BaseModel
from pydantic.networks import EmailStr
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserRegister(UserBase):
    password: str


class UserUpdateIn(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        orm_mode = True


class UserToken(BaseModel):
    id: int
    email: EmailStr


class UserUpdatePassword(BaseModel):
    password: str


class UserUpdateOut(UserUpdateIn):
    created_date: Optional[datetime]
    updated_at: Optional[datetime]
