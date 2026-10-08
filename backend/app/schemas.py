from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: Optional[str]
    credits_remaining: int
    plan: str
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Video Schemas
class GenerateVideoRequest(BaseModel):
    prompt: str = Field(..., min_length=5, max_length=500)
    style: str = Field(default="cinematic")
    duration: int = Field(default=5, ge=3, le=10)
    aspect_ratio: str = Field(default="9:16")

class VideoResponse(BaseModel):
    id: str
    user_id: str
    prompt: str
    style: str
    duration: int
    aspect_ratio: str
    status: str
    output_url: Optional[str]
    thumbnail_url: Optional[str]
    model_name: str
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class VideoListResponse(BaseModel):
    total: int
    videos: list[VideoResponse]
