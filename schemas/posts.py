from datetime import datetime
from schemas.images import Image
from .users import User
from pydantic import BaseModel
from fastapi import UploadFile
from typing import List

class BasePost(BaseModel):
    images_url: List[UploadFile]

class Post(BaseModel):
    id: str
    user: User
    point: float
    rank_post: int
    rank_user: int
    images: List[Image]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True