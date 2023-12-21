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
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading cache from file {filename}: {e}")
        return None
    

def write_cache(filename, data):
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(filename, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        print(f"Error writing cache to file {filename}: {e}")


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
    try: 
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
    except requests.exceptions.RequestException as e:
        print(f"Request error for symbol {symbol}: {e}")
        return None
    except ValueError as e:
        print(f"Value error: could not convert data to float for symbol {symbol}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred for symbol {symbol}: {e}")
        return None

@app.route('/')
def index():
    total_value = 0
    prices = {}
    errors = {}
    for stock, quantity in stocks.items():
        price = get_stock_prices(stock)
        if price is not None:
            total_value += price * quantity
            prices[stock] = price
        else:
            # Handle the scenario where price is None
            errors[stock] = "Price data unavailable"
            prices[stock] = "N/A"  # You can set a placeholder like "N/A" or 0

    return render_template('index.html', prices=prices, total=total_value, stocks=stocks, errors=errors)


if __name__ == '__main__':
    app.run(debug=True)