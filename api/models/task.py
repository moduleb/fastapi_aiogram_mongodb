from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime
from sqlalchemy.ext.declarative import declarative_base

from api.database import engine

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name: str = Column(String, nullable=False, unique=True)
    creation_date: datetime = Column(DateTime, default=str(datetime.now()))
    price: Optional[DECIMAL] = Column(DECIMAL(precision=10, scale=2))
    # DECIMAL(precision=8, scale=2) --> всего 10 цифр, два знака после запятой (напр. 99.999.999)

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)