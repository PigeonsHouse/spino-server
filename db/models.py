from requests.api import post
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime

from utils import gen_primarykey
from .base import Base

class User(Base):
  id = Column(String, default=gen_primarykey, primary_key=True, index=True)
  name = Column(String, unique=False, index=True)
  img = Column(String, unique=False, index=True)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)

  post = relationship(
    'Post', back_populates="user"
  )

  top_post = relationship(
    'TopPost', back_populates="user"
  )

class TopPost(Base):
  id = Column(String, default=gen_primarykey, primary_key=True, index=True)
  point = Column(Integer, unique=False, index=True)
  user_id = Column(String, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  image_url = Column(String, index=True)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)

  user = relationship(
    'User', back_populates="top_post"
  )

class Post(Base):
  id = Column(String, default=gen_primarykey, primary_key=True, index=True)
  point = Column(Integer, unique=False, index=True)
  user_id = Column(String, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  image_url = Column(String, index=True)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)

  user = relationship(
    'User', back_populates="post"
  )
