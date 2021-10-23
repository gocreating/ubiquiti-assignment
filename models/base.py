from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from db import Database


class BaseClass:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, index=True, server_default=func.now())
    updated_at = Column(DateTime, index=True, server_default=func.now(), onupdate=func.now())

Base = declarative_base(cls=BaseClass, metadata=Database.get_metadata())
