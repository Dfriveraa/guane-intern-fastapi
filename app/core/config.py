from functools import lru_cache

from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    app_name: str
    database_url: AnyUrl
    jwt_token: str
    api_image: str
    database_testing: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
