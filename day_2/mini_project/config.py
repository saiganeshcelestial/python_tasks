from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "TaskAPI"
    DEBUG: bool = False
    JSON_DB_PATH: str = "./data"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "changeme"

    model_config = SettingsConfigDict(env_file=".env")


# Singleton
settings = Settings()
