from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    ORACLE_DB_USERNAME : str 
    ORACLE_DB_PASSWORD: str
    ORACLE_DB_DSN: str

    # openssl rand -hex 32
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRATION_MINUTES : int

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()