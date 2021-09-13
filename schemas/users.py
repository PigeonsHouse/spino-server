from pydantic import BaseModel, EmailStr
from datetime import datetime

class BaseUser(BaseModel):
    name: str
    email: EmailStr

class User(BaseUser):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
