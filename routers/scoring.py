from schemas.ComputerVision import ComputerVisionResponse
from cruds.posts import image_scoring
from typing import List
from pydantic import HttpUrl
from schemas.posts import Post
from db import get_db
from fastapi import APIRouter
from sqlalchemy.orm.session import Session
from fastapi.params import Depends
from schemas.users import User

scoring_router = APIRouter()

@scoring_router.post('/scoring', response_model=List[ComputerVisionResponse])
async def post_scoring(payload: List[HttpUrl], db: Session = Depends(get_db)):# , user = Depends(get_current_user)):
    image_responces = image_scoring(payload)
    
    return image_responces