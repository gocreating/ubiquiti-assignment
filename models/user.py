from sqlalchemy import Column, String

from models.base import Base


class User(Base):
    __tablename__ = 'users'

    acct = Column(String)
    pwd = Column(String)
    fullname = Column(String)
