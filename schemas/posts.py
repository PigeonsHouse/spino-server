from datetime import datetime
from pydantic.networks import HttpUrl
from .users import User
from pydantic import BaseModel
from typing import Optional

class CreatingPost(BaseModel):
    image_url: str 

class Post(BaseModel):
    id: str
    user: User
    point: float
    rank: Optional[int]
    image_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True