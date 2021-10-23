from __future__ import annotations
import jwt
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import Column, String

from config import JWT_SECRET
from models.base import Base


class User(Base):
    __tablename__ = 'users'

    acct = Column(String)
    pwd = Column(String)
    fullname = Column(String)

    @staticmethod
    def get_by_jwt(session, encoded_jwt: str) -> Optional[User]:
        jwt_payload = jwt.decode(encoded_jwt, JWT_SECRET, algorithms='HS256')
        user = session.query(User).get(jwt_payload['user']['id'])
        return user

    def generate_jwt(self) -> str:
        jwt_payload = {
            'exp': datetime.utcnow() + timedelta(days=14),
            'user': {
                'id': self.id
            }
        }
        token = jwt.encode(jwt_payload, JWT_SECRET, algorithm='HS256')
        return token

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            'acct': self.acct,
            'fullname': self.fullname,
        }
