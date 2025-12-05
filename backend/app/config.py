from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    database_url: str = "postgresql://wealth_user:wealth_password@localhost:5432/wealth_assets"
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

