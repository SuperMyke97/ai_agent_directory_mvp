from sqlalchemy import Column,Integer, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from database import BaseModel, init_db
from agents import Agent
from users import User


class Rating(BaseModel): # type: ignore

    __tablename__ = "ratings"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"))
    value = Column(Integer, nullable=False)

    user = relationship("User", back_populates="ratings")
    agent = relationship("Agent", back_populates="ratings")

    __table_args__ = (UniqueConstraint("user_id", "agent_id", name="_user_agent_ratings_uc"),
                      CheckConstraint("value >= 1 AND value <=5", name="_check_rating_range"))


init_db()