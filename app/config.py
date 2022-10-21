from pydantic import BaseSettings


class Settings(BaseSettings):
    alphavantage_apikey: str = ''
    alphavantage_url: str = 'https://www.alphavantage.co/query'


settings = Settings()
