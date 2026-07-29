from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "adder-app"
    log_level: str = "INFO"
    log_json: bool = True
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    cors_origins: list[str] = ["http://localhost:8000"]

settings = Settings()