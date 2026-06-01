from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.infrastructure.persistence.postgresql.database import Base

class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
