from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class BaseUser(BaseModel):
    name: str
    img: str

class PutUser(BaseModel):
    name: Optional[str]
    img: Optional[str]

class User(BaseUser):
    id: str
    img: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RankingUser(User):
    rank: Optional[int]
    high_score: Optional[int]