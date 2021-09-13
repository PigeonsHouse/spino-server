from datetime import datetime
from .posts import Post
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    id: str
    url: HttpUrl
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
