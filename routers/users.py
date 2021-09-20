from fastapi import APIRouter
from db import models, get_db
from schemas.users import BaseUser
from sqlalchemy.orm.session import Session
from fastapi import FastAPI, Depends, HTTPException, status
from cruds.users import get_current_user_id, _get_user

user_router = APIRouter()

@user_router.get('/users/me')
async def get_me(db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user_id)):
    user = _get_user(db, current_user_id)
    return user