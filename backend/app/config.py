import os
from datetime import timedelta, datetime
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    app_name: str = "VividMotion AI"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    
    # Security & JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Database
    database_url: str = "sqlite:///./test.db"
    
    # AI Video Providers
    video_model_provider: str = "mock"  # mock, replicate, runway, stability
    replicate_api_key: str = ""
    runway_api_key: str = ""
    stability_api_key: str = ""
    openai_api_key: str = ""
    
    # Storage
    storage_provider: str = "local"  # local, s3, supabase
    s3_bucket: str = ""
    s3_region: str = "us-east-1"
    s3_access_key: str = ""
    s3_secret_key: str = ""
    
    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Stripe (future)
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
