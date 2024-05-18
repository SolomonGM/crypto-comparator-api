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
    
    #Response call to fecth prices from coingecko api
    repsonse = repsonse.get(COINGECKO_API_URL, params=params)
    
    #validate reponse with code 
    if repsonse.status_code == 200:
        data = repsonse.json()
        for crypto in SUPPORTED_COINS:
            if crypto in data and 'usd' in data[crypto]:
                prices[crypto] = round(data[crypto]['usd'], 2)
            else:
                prices[crypto] = None
    else:
        raise HTTPException(status_code=repsonse.status_code, detail="Error while fetching information from CoinGecko")            

def start_schedular():
    #Initialise a schedular that fetches prices every 5 mins
    schedular = BackgroundScheduler()
    schedular.add_job(fetch_prices, 'interval', minutes=5)
    schedular.start()

@app.on_event("startup")
def startup_event():
    threading.Thread(target=start_schedular).start()
    fetch_prices()
    
@app.get("/")
def read_root():
    return {"message": "Crypto to Currency Comparator API"}

@app.get("/compare/{crypto_id}/{fiat_currency}")
def compare_crypto_to_currency(crypto_id: str, fiat_currency: str):
    if crypto_id not in SUPPORTED_COINS or fiat_currency not in SUPPORTED_FIATS:
        raise HTTPException(status_code=404, detail="Cryptocurrency or currency not supported")
    
    if crypto_id not in prices or prices[crypto_id] is None:
        raise HTTPException(status_code=404, detail="Price not available")
    
    return {
        "crypto_id": crypto_id,
        "fiat_currency": fiat_currency,
        "value": f"{prices[crypto_id]:.2f}"
    }

@app.get("/compare")
def compare_multiple_cryptos(crypto_ids: str, fiat_currency: str):
    if fiat_currency not in SUPPORTED_FIATS:
        raise HTTPException(status_code=404, detail="Currency not supported")
    
    ids = crypto_ids.split(',')
    result = {}
    
    for crypto_id in ids:
        if crypto_id in SUPPORTED_COINS:
            if crypto_id in prices and prices[crypto_id] is not None:
                result[crypto_id] = f"{prices[crypto_id]:.2f}"
            else:
                result[crypto_id] = "Prices not available"
        else:
            result[crypto_id] = "Not supported"
            
    return result
