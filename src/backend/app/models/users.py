from sqlalchemy import Column,Integer, String,Text, Boolean, DateTime, func, Index, ForeignKey,CheckConstraint, UniqueConstraint
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



class Highlight(BaseModel): # type: ignore

    __tablename__ = "highlights"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="highlights")
    agent = relationship("Agent", back_populates="highlights")

    __table_args__ = (UniqueConstraint("user_id", "agent_id", name="_user_agent_highlight_uc"),)


class Review(BaseModel): # type: ignore

    __tablename__ = "reviews"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"))
    content = Column(Text)

    user = relationship("User", back_populates="reviews")
    agent = relationship("Agent", back_populates="reviews")

    __table_args__ = (Index("idx_reviews_user_agent","user_id", "agent_id"),)


class Rating(BaseModel): # type: ignore

    __tablename__ = "ratings"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="CASCADE"))
    value = Column(Integer, nullable=False)

    user = relationship("User", back_populates="ratings")
    agent = relationship("Agent", back_populates="ratings")

    __table_args__ = (UniqueConstraint("user_id", "agent_id", name="_user_agent_ratings_uc"),
                      CheckConstraint("value >= 1 AND value <=5", name="_check_rating_range"))


class Agent(BaseModel):

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

    __table_args__ = (Index("idx_agent_category_created_at", "category", "created_at"),)


