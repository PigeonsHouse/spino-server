from fastapi import APIRouter
# from schemas.user import User, CreateUser
from db import models, get_db
from schemas.users import BaseUser, PutUser
from sqlalchemy.orm.session import Session
from fastapi import FastAPI, Depends, HTTPException, status
from cruds.users import create_user, get_current_user_id, change_info

sign_router = APIRouter()

@sign_router.post('/signup')
def post(payload: BaseUser, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user_id)):
    user = create_user(db, payload.name, payload.img, current_user_id)
    return user

@sign_router.put('/signup')
def change_user_info(payload: PutUser, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user_id)):
    user = change_info(db, payload, current_user_id)
    return user