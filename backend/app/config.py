from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App settings
    app_name: str = "VividMotion AI"
    api_v1_prefix: str = "/api"
    debug: bool = False
    
    # Database
    postgres_url: str = "postgresql://postgres:postgres@localhost:5432/vividmotion"
    
    # AI Video Model Providers
    video_model_provider: str = "mock"  # mock, replicate, runway, stability
    
    # Replicate API
    replicate_api_key: str = ""
    
    # Runway API
    runway_api_key: str = ""
    
    # Stability AI
    stability_api_key: str = ""
    
    # OpenAI (for prompt enhancement)
    openai_api_key: str = ""
    
    # Storage
    s3_bucket: str = ""
    s3_region: str = "us-east-1"
    s3_access_key: str = ""
    s3_secret_key: str = ""
    
    # Supabase alternative
    supabase_url: str = ""
    supabase_key: str = ""
    
    # Redis (for job queue)
    redis_url: str = "redis://localhost:6379"
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
