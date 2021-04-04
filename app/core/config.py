from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str
    host: str
    database: str
    user_db: str
    password_db: str
    port_db: str
    jwt_token: str
    api_image: str
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
