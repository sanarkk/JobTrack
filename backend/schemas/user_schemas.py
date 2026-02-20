from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserOut(UserBase):
    id: str
    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        data = dict(obj.__dict__)
        data['id'] = str(obj.id)
        return cls(**data)
