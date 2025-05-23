from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(String, unique=True, nullable=False)
    token_symbol = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    post_weight = Column(Integer, nullable=False)
    tweet_text = Column(String, nullable=False)
    tweet_created_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    num_of_share = Column(Integer, nullable=False)
    num_of_like = Column(Integer, nullable=False)
    num_of_comment = Column(Integer, nullable=False)
    num_of_normal_user_retweet = Column(Integer, nullable=False)
    num_of_verified_user_retweet = Column(Integer, nullable=False)
    num_of_famous_user_retweet = Column(Integer, nullable=False)
