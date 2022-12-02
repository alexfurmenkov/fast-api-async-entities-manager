import uuid

from sqlalchemy import Column, Integer, String

from .base_model import BaseModel


class UserDBModel(BaseModel):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
