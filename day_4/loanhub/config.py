from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LoanHub"
    debug: bool = False
    database_url: str
    log_level: str = "INFO"
    pool_size: int = 5
    max_overflow: int = 10
    admin_username: str = "admin"
    admin_password: str
    admin_email: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
