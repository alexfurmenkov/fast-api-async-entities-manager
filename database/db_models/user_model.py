from sqlalchemy import Column, Integer, String, UniqueConstraint

from .base_model import BaseModel


class UserDBModel(BaseModel):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint('username', name='_username_unique_constraint'), )

    id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
