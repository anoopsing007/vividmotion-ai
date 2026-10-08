from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "VividMotion AI"
    api_v1_prefix: str = "/api"
    openai_api_key: str = ""
    postgres_url: str = "postgresql://postgres:postgres@localhost:5432/vividmotion"
    video_model_provider: str = "mock"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
