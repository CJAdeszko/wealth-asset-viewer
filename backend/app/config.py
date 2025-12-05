from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    database_url: str = "postgresql://wealth_user:wealth_password@localhost:5432/wealth_assets"
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    
    # CORS settings (comma-separated list of origins, or "*" for all)
    cors_origins_str: str = "*"
    
    @property
    def cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        if self.cors_origins_str == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins_str.split(",")]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

