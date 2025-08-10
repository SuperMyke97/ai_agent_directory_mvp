from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Index
from sqlalchemy.orm import relationship
from backend.app.database import BaseModel, init_db


class User(BaseModel): # type: ignore

    __tablename__ = "users"
    full_name = Column(String(200), nullable=False)
    username = Column(String(200),unique=True,nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    disabled = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    hash_password = Column(String(200), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())  
    last_login = Column(DateTime, nullable=True)

    # Index for username and email for faster lookups
    __table_args__ = (Index("idx_user_username_email", "username", "email"),)

    
    # Relationships
    highlights = relationship("Highlight", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")


init_db()