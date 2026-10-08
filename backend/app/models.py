from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    credits_remaining = Column(Integer, default=10)
    plan = Column(String, default="free")  # free, pro, business
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    videos = relationship("Video", back_populates="user")
    api_keys = relationship("APIKey", back_populates="user")

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    prompt = Column(Text, nullable=False)
    style = Column(String, default="cinematic")
    duration = Column(Integer, default=5)
    aspect_ratio = Column(String, default="9:16")
    status = Column(String, default="processing")  # processing, completed, failed
    output_url = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    model_name = Column(String, default="stable-video-diffusion")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="videos")

class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    key = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="api_keys")

class VerificationToken(Base):
    __tablename__ = "verification_tokens"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
