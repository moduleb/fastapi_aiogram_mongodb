from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from api.database import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String, unique=True, nullable=False, index=True)
    password: str = Column(String, nullable=False)

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)