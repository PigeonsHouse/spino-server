from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import r
from db import engine
from db.base import Base

Base.metadata.create_all(engine)

print('Hello')

app = FastAPI(
  title='spino-server'
)

# Set all CORS enabled origins
app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

app.include_router(r, prefix='/api/v1')