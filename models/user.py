from sqlalchemy import Column, String

from models.base import Base


class User(Base):
    __tablename__ = 'users'

    acct = Column(String)
    pwd = Column(String)
    fullname = Column(String)

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            'acct': self.acct,
            'fullname': self.fullname,
        }
