from flask import Flask, render_template
import requests
import json
import os 
import time


app = Flask(__name__)

# Alpha Vantage API details
API_URL = "https://www.alphavantage.co/query"
API_KEY = "Z26IND1A7LZTHK7V"

# Caching
CACHE_DIR = "cache"
CACHE_DURATION = 600


def cache_filename(symbol):
    return os.path.join(CACHE_DIR, f"{symbol}.json")


def is_cache_valid(filename):
    if not os.path.exists(filename):
        return False
    if time.time() - os.path.getmtime(filename) > CACHE_DURATION:
        return False
    return True


def read_cache(filename):
    with open(filename, 'r') as file:
        return json.load(file)
    

def write_cache(filename, data):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(filename, 'w') as file:
        json.dump(data, file)


stocks = {
    "TSLA": 16,
    "GOOGL": 20,
    "AMZN": 20,
    "AAPL": 14,
    "CSCO": 1,
    "NOK": 2
}

# Function to get stock prices
def get_stock_prices(symbol):
    # Caching logic here
    filename = cache_filename(symbol)
    if is_cache_valid(filename):
        return read_cache(filename)["price"]
    
    response = requests.get(API_URL, {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    })
    data = response.json()
    print(data)
    price = float(data["Global Quote"]["05. price"])

    # Write new data to cache
    write_cache(filename, {"price": price})

    return price


@app.route('/')
def index():
    total_value = 0
    prices = {}
    for stock, quantity in stocks.items():
        price = get_stock_prices(stock)
        total_value += price * quantity
        prices[stock] = price
    return render_template('index.html', prices=prices, total=total_value, stocks=stocks)


if __name__ == '__main__':
    app.run(debug=True)