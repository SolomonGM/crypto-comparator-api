from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import threading

app = FastAPI()

COINGECKO_API_URL = "https://www.coingecko.com/en/all-cryptocurrencies"
SUPPORTED_COINS = ["bitcoin", 'ethereum', 'litcoin', 'usdt']
SUPPORTED_FIATS = ['usd']
prices = {}

def fetch_prices():
    global prices
    params = {
        'ids': ','.join(SUPPORTED_COINS),
        'vs_currencies': ','.join(SUPPORTED_FIATS)
    }
    
    repsonse = repsonse.get(COINGECKO_API_URL, params=params)

app = FastAPI()

@app.get("/")

def root():
    return {"Hello": "World"}
