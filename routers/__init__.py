from fastapi import APIRouter
from .sign import sign_router
from .scoring import scoring_router
from .ranking import ranking_router
from .users import user_router
from .posts import post_router

r = APIRouter()
r.include_router(sign_router)
r.include_router(scoring_router)
r.include_router(ranking_router)
r.include_router(user_router)
r.include_router(post_router)
