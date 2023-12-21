# Stock Portfolio Web Application

This Flask web application fetches real-time stock prices using the Alpha Vantage API and displays them along with the total value of a predefined stock portfolio. It features server-side caching to optimize API usage and improve performance.

## Features
- Real-Time Stock Prices: Fetches the latest prices for a set of stocks.
- Portfolio Management: Displays quantities and total values of selected stocks.
- Server-Side Caching: Implements file-based caching to limit API calls.
- User-Friendly Interface: Presents data in a neatly formatted table.

## Setup and Installation
1. Clone the Repository
```bash
git clone [repository_url]
cd [repository_name]
```
2. Create and Activate a Virtual Environment (optional, but recommended)
- For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
- For macOS and Linux:
```bash 
python3 -m venv venv
source venv/bin/activate
```
3. Install Dependencies:
```bash
pip install Flask requests
```
4. Set Environment Variables
- For Windows:
```bash 
set FLASK_APP=app.py
set FLASK_ENV=development
```

- For macOS and Linux:
```bash 
export FLASK_APP=app.py
export FLASK_ENV=development
```
5. Run the Application
```bash
flask run
```

## Usage
- Access the web application via http://127.0.0.1:5000 in your web browser.
- View real-time stock prices and the total value of the stock portfolio.

# File Structure
- app.py: Main Flask application file.
- templates/: Folder containing HTML templates.
  - index.html: The main template for displaying stock prices.
- static/: Folder for static files.
  - style.css: CSS stylesheet for styling the web interface.

# Caching Mechanism
- Caching is implemented to reduce the frequency of API calls.
- Stock prices are stored in the cache directory with a defined expiration time.
- Cached data is used when available and not expired; otherwise, an API call is made.