from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from starlette.exceptions import HTTPException

user_router = APIRouter()
