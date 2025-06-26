from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from database import BaseModel, init_db


class Agent(BaseModel): # type: ignore

    __tablename__ = "agents"
    name = Column(String(200),unique=True,nullable=False)
    description = Column(String(1000))
    category = Column(String(200))
    homepage_url = Column(String(1000))
    source = Column(String(1000))
    trending = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    highlights = relationship("Highlight", back_populates="agent", cascade="all, delete")
    reviews = relationship("Review", back_populates="agent", cascade="all, delete")
    ratings = relationship("Rating", back_populates="agent", cascade="all, delete")


init_db()