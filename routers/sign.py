from fastapi import APIRouter
# from schemas.user import User, CreateUser
from db import models, get_db
from schemas.users import BaseUser
from sqlalchemy.orm.session import Session
from fastapi import FastAPI, Depends, HTTPException, status
from cruds.users import create_user, get_current_user_id

sign_router = APIRouter()

@sign_router.post('/signup')
def post(payload: BaseUser, db: Session = Depends(get_db), current_user: str = Depends(get_current_user_id)):
    user = create_user(db, payload.name, current_user)
    return user