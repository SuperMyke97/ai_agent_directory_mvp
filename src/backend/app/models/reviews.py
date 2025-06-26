from sqlalchemy import Column,Integer, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from database import BaseModel, init_db
from agents import Agent
from users import User


class Review(BaseModel): # type: ignore

    __tablename__ = "reviews"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"))
    content = Column(Text)

    user = relationship("User", back_populates="reviews")
    agent = relationship("Agent", back_populates="reviews")

    __table_args__ = (Index("idx_reviews_user_agent","user_id", "agent_id"),)


init_db()