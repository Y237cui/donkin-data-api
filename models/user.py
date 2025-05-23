from typing import List, Optional

from sqlalchemy import ARRAY, BigInteger, Boolean, Column, DateTime, Double, ForeignKeyConstraint, Index, Integer, JSON, PrimaryKeyConstraint, Sequence, SmallInteger, String, Table, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass
class KolUsers(Base):
    __tablename__ = 'kol_users'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='kol_users_pkey'),
    )
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="twitter's userid")
    user_name: Mapped[str] = mapped_column(String(255), comment="twitter's username")
    user_type: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'), comment='0: normal')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 6))
    kol_rank: Mapped[Optional[int]] = mapped_column(Integer, comment='rank of kol')

class KolTweets(Base):
    __tablename__ = 'kol_tweets'
    __table_args__ = (
        PrimaryKeyConstraint('tweet_id', name='kol_tweets_pkey'),
    )

    user_id: Mapped[int] = mapped_column(BigInteger, comment="twitter's userid")
    tweet_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="twitter's tweet id")
    type: Mapped[str] = mapped_column(String(255), comment='tweet, photo')
    url: Mapped[Optional[str]] = mapped_column(String(255))
    twitter_url: Mapped[Optional[str]] = mapped_column(String(255))
    text_: Mapped[Optional[str]] = mapped_column('text', Text)
    quoted_tweet_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 6))
    tweet_created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 6))
    lang: Mapped[Optional[str]] = mapped_column(String(255), comment="text's language")

t_kol_extras = Table(
    'kol_extras', Base.metadata,
    Column('source', String(255), nullable=False, comment="table's"),
    Column('tid', String(255), nullable=False, comment='string type id in the table'),
    Column('content', JSON, comment='json content'),
    Column('created_at', TIMESTAMP(True, 6)),
    Column('updated_at', TIMESTAMP(True, 6))
)

class KolTweetAnalysis(Base):
    __tablename__ = 'kol_tweet_analysis'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='kol_tweet_analysis_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tweets_ids: Mapped[str] = mapped_column(Text, comment='comma separate list')
    analysis_detail: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 6))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 6))
    earliest_tweet_time: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 6))
    latest_tweet_time: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 6))
    version: Mapped[Optional[str]] = mapped_column(String(255))
    token_address: Mapped[Optional[str]] = mapped_column(String(255))
    time_unit: Mapped[Optional[str]] = mapped_column(String(255), comment='1d, 30m')
    token_name: Mapped[Optional[str]] = mapped_column(String(255))
    token_symbol: Mapped[Optional[str]] = mapped_column(String(255))

class TokenInfo(Base):
    __tablename__ = 'token_info'
    __table_args__ = (
        PrimaryKeyConstraint('address', name='token_info_pkey'),
    )

    address: Mapped[str] = mapped_column(Text, primary_key=True, comment='代币合约地址')
    chain_id: Mapped[Optional[int]] = mapped_column(Integer)
    symbol: Mapped[Optional[str]] = mapped_column(Text, comment='代币符号')
    name: Mapped[Optional[str]] = mapped_column(Text, comment='代币名称')
    decimals: Mapped[Optional[int]] = mapped_column(Integer, comment='代币精度')
    logo_uri: Mapped[Optional[str]] = mapped_column(Text, comment='代币图标链接')
    tags: Mapped[Optional[list]] = mapped_column(ARRAY(Text()), comment='代币标签')
    total_supply: Mapped[Optional[str]] = mapped_column(Text, comment='代币总量')
    price: Mapped[Optional[float]] = mapped_column(Double(53), comment='代币价格')
    daily_volume: Mapped[Optional[float]] = mapped_column(Double(53))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    freeze_authority: Mapped[Optional[str]] = mapped_column(Text)
    mint_authority: Mapped[Optional[str]] = mapped_column(Text)
    permanent_delegate: Mapped[Optional[str]] = mapped_column(Text)
    minted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), comment='代币创建时间')
    coingecko_id: Mapped[Optional[str]] = mapped_column(Text)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    market_cap: Mapped[Optional[float]] = mapped_column(Double(53), comment='代币市值')
    price_change_24h: Mapped[Optional[float]] = mapped_column(Double(53), comment='24小时价格变化万分比')
    volume_24h: Mapped[Optional[float]] = mapped_column(Double(53))
    last_trade_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    liquidity: Mapped[Optional[float]] = mapped_column(Double(53), comment='流动性池')
    volume_change_24h: Mapped[Optional[float]] = mapped_column(Double(53), comment='24小时交易量变化百分比')
    rank: Mapped[Optional[int]] = mapped_column(Integer, comment='代币排名')
    fdv: Mapped[Optional[float]] = mapped_column(Double(53), comment='完全稀释估值 (Fully Diluted Valuation)')
    creation_unix_time: Mapped[Optional[int]] = mapped_column(BigInteger, comment='代币创建时间（Unix时间戳）')
    creation_human_time: Mapped[Optional[str]] = mapped_column(Text, comment='代币创建时间（人类可读格式）')
