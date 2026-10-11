from functools import lru_cache

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file='.env', env_file_encoding='utf-8')

    app_name: str = Field(default='booking-service')
    app_env: str = Field(default='development')
    database_url: str = Field(default='postgresql+psycopg://postgres:postgres@localhost:5432/booking_db')


@lru_cache
def get_settings() -> Settings:
    return Settings()
