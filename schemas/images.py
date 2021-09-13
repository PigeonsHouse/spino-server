from datetime import datetime
from .posts import Post
from pydantic import BaseModel, HttpUrl

class BaseImage(BaseModel):
    url: HttpUrl
    post: Post

class Post(BaseImage):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
