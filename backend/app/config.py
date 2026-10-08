from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "VividMotion AI"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    database_url: str = "sqlite:///./vividmotion.db"

    video_model_provider: str = "mock"
    replicate_api_key: str = ""
    runway_api_key: str = ""
    stability_api_key: str = ""
    openai_api_key: str = ""

    storage_provider: str = "local"
    s3_bucket: str = ""
    s3_region: str = "us-east-1"
    s3_access_key: str = ""
    s3_secret_key: str = ""

    supabase_url: str = ""
    supabase_key: str = ""

    redis_url: str = "redis://localhost:6379"
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:3001"]

    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
