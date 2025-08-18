from sqlalchemy import Column,Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.database import BaseModel, init_db


class Highlight(BaseModel): # type: ignore

    __tablename__ = "highlights"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="highlights")
    agent = relationship("Agent", back_populates="highlights")

    __table_args__ = (UniqueConstraint("user_id", "agent_id", name="_user_agent_highlight_uc"),)

init_db()
