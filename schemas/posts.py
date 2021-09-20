from datetime import datetime
from schemas.images import Image
from .users import User
from pydantic import BaseModel
from typing import List, Optional

class Post(BaseModel):
    id: str
    user: User
    point: float
    rank_post: Optional[int]
    rank_user: Optional[int]
    images: Optional[List[Image]]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True