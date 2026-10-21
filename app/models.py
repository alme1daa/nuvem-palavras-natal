from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base

class WordSubmission(Base):
    __tablename__ = "word_submissions"
    id = Column(Integer, primary_key=True, index=True)
    raw_word = Column(String(50), nullable=False)
    normalized_word = Column(String(50), nullable=False, index=True)
    status = Column(String(20), default="pending", index=True)
    ip_address = Column(String(45), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class WordAggregate(Base):
    __tablename__ = "word_aggregates"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(50), unique=True, nullable=False, index=True)
    frequency = Column(Integer, default=1)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ConfigSetting(Base):
    __tablename__ = "config_settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, nullable=False)
    value_bool = Column(Boolean, nullable=True)
    value_text = Column(String(500), nullable=True)

class AllowedWord(Base):
    __tablename__ = "allowed_words"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(50), unique=True, nullable=False)

class BlockedWord(Base):
    __tablename__ = "blocked_words"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(50), unique=True, nullable=False)