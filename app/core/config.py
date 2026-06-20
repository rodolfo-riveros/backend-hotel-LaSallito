from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Hotel IES La Salle - PMS"
    debug: bool = False
    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
