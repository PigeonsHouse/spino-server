from fastapi import APIRouter
from .users import user_router

r = APIRouter()
r.include_router(user_router, prefix='/users', tags=['users'])