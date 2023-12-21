from flask import Flask, render_template
import requests
import json
import os 
import time


app = Flask(__name__)

# Alpha Vantage API details
API_URL = "https://www.alphavantage.co/query"
API_KEY = ""

# Caching
CACHE_DIR = "cache"
CACHE_DURATION = 3600


def cache_filename(symbol):
    try:
        return os.path.join(CACHE_DIR, f"{symbol}.json")
    except Exception as e:
        print(f"Error generating cache filename for symbol {symbol}: {e}")
        return None


def is_cache_valid(filename):
    try:
        if not os.path.exists(filename):
            return False
        if time.time() - os.path.getmtime(filename) > CACHE_DURATION:
            return False
        return True
    except Exception as e:
        print(f"Error checking cache validity for file {filename}: {e}")
        return False


def read_cache(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def write_cache(filename, data):
    cache_data = {
        "price": data,
        "timestamp": time.time()
    }
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(filename, 'w') as file:
        json.dump(cache_data, file)


stocks = {
    "TSLA": 16,
    "GOOGL": 20,
    "AMZN": 20,
    "AAPL": 14,
    "CSCO": 1,
    "NOK": 2
}

def get_stock_prices(symbol):
    filename = cache_filename(symbol)

    try:
        # Attempt to make an API call first
        response = requests.get(API_URL, {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": API_KEY
        })
        response.raise_for_status()  # Raises an error for bad status codes
        data = response.json()

        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            price = float(data["Global Quote"]["05. price"])
            # Successful API call, write data to cache
            write_cache(filename, price)
            return price, time.time()
        else:
            # Data not in expected format, fallback to cache
            print(f"Unexpected data format for {symbol}: {data}")
            cache_data = read_cache(filename) if os.path.exists(filename) else {"price": None}
            return cache_data["price"], cache_data.get("timestamp")

    except requests.exceptions.RequestException as e:
        # API call failed, fallback to cache
        print(f"Request error for symbol {symbol}: {e}")
        cache_data = read_cache(filename) if os.path.exists(filename) else {"price": None}
        return cache_data["price"], cache_data.get("timestamp")
    except Exception as e:
        print(f"An unexpected error occurred for symbol {symbol}: {e}")
        return None, None


@app.route('/')
def index():
    total_value = 0
    prices = {}
    timestamps = {}
    for stock, quantity in stocks.items():
        price, timestamp = get_stock_prices(stock)
        if price is not None:
            total_value += price * quantity
        prices[stock] = price if price is not None else "N/A"
        timestamps[stock] = timestamp

    return render_template('index.html', prices=prices, total=total_value, stocks=stocks, timestamps=timestamps)


if __name__ == '__main__':
    app.run(debug=True)