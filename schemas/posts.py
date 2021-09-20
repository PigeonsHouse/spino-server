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
    rank_post: Optional[int]
    rank_user: Optional[int]
    image_url: HttpUrl
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True