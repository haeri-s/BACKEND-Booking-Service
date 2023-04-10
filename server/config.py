from pydantic import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os
load_dotenv(verbose=True)

class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME")
    jwt_setting: dict = {
      "secret_key":os.getenv('SECRET_KEY'),
      "algorithm": os.getenv('ALGORITHM'),
      "expire_days": int(os.getenv('ACCESS_TOKEN_EXPIRE_DAYS', 7)),
    }
    db_url: str = os.getenv('DATABASE_URL')

    class Config:
        env_prefix = ''
        env_file = "../.env"


@lru_cache()
def get_settings():
    return Settings()