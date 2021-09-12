
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
  password_hash = Column(String, nullable=False)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)
