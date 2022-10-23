from pydantic import BaseSettings


class Settings(BaseSettings):
    alphavantage_apikey: str
    alphavantage_url: str = 'https://www.alphavantage.co/query'
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int = 5432


settings = Settings()
