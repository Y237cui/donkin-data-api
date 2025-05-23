from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Reply(Base):
    __tablename__ = 'replies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(String, unique=True, nullable=False)
    user_id = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    comment_text = Column(String, nullable=False)
    comment_created_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    reply_to_tweet_id = Column(String, nullable=False)
