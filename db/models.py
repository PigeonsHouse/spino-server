
from enum import Enum
from sqlalchemy.schema import Sequence
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Interval
from datetime import datetime
from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.elements import Case
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.sqltypes import DATE, Float
from utils import gen_primarykey
from .base import Base

class User(Base):
  id = Column(String, default=gen_primarykey, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True, nullable=False)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)

class Post(Base):
  id = Column(String, default=gen_primarykey, primary_key=True, index=True)
  point = Column(Integer, unique=True, index=True)
  user_id = Column(String, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)

  user = relationship(
    'User',
  )

  images = relationship(
    'Image',
  )

  seen_users = relationship(
    'User',
    secondary='seen',
  )

  favorited_users = relationship(
    'User',
    secondary='favorite',
  )


class Image(Base):
  id = Column(String, default=gen_primarykey, primary_key=True, index=True)
  url = Column(String, unique=True, index=True)
  post_id = Column(String, ForeignKey('post.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)
  
