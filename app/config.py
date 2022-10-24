import sys
from pydantic import BaseSettings


class Settings(BaseSettings):
    alphavantage_apikey: str
    alphavantage_url: str = 'https://www.alphavantage.co/query'
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int = 5432
    secret_key: str
    salt: str
    redis: str = 'cache' if 'pytest' not in sys.modules else 'cache_test'


settings = Settings()
