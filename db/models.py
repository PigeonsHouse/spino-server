from sqlalchemy import Column, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from utils import gen_primarykey
from .base import Base

class User(Base):
  id = Column(String, default=gen_primarykey, primary_key=True, index=True)
  name = Column(String, unique=True, index=True)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)

class Post(Base):
  id = Column(String, default=gen_primarykey, primary_key=True, index=True)
  point = Column(Float, unique=False, index=True)
  user_id = Column(String, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)

  user = relationship(
    'User',
  )
  images = relationship(
    'Image', back_populates='post'
  )

class Image(Base):
  id = Column(String, default=gen_primarykey, primary_key=True, index=True)
  url = Column(String, index=True)
  post_id = Column(String, ForeignKey('post.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)
  
  post = relationship(
    'Post', back_populates='images'
  )
