from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import BaseModel, init_db


class User(BaseModel): # type: ignore

    __tablename__ = "users"
    username = Column(String(200),unique=True,nullable=False)
    email = Column(String(200),unique=True,nullable=False)
    hash_password = Column(String(200),nullable=False)
    is_admin = Column(Boolean, default=False)

    highlights = relationship("Highlight", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")


init_db()