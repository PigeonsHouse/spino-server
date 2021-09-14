from fastapi import APIRouter
# from schemas.user import User, CreateUser
from fastapi import FastAPI, Depends, HTTPException, status
from cruds.users import create_user, get_current_user

sign_router = APIRouter()

@sign_router.post('/signup')
def post(current_user=Depends(get_current_user)):
    return {'msg': 'ok', 'user': current_user}