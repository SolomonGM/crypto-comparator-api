import os
from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    coingecko_api_url: str = "https://www.coingecko.com/en/all-cryptocurrencies"
    supported_coins: List[str] = ["bitcoin", 'ethereum', 'litcoin', 'usdt', '']
    supported_fiats: List[str] = ['usd']
    update_intervals: int = 5 # Update the coin fetch in minutes
    
    class Config:
        env_file = ".env"

settings = Settings()
