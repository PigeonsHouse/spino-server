from datetime import datetime
from .users import User
from pydantic import BaseModel

class BasePost(BaseModel):
    point: float
    user: User

class Post(BasePost):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True