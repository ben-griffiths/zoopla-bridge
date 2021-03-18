from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    """Data model for users"""

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
    )
    created = Column(DateTime, index=False, unique=False, nullable=False)

    def __repr__(self):
        return "<User {}>".format(self.id)
