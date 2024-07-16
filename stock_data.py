# File: Portfolio_Tracker/stock_data.py
# Description: Module for fetching stock data from external APIs.

import requests
from config import Config

def get_stock_quote(symbol):
    """Fetch the current stock quote for a given symbol."""
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={Config.ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return {
        'symbol': symbol,
        'price': float(data['Global Quote']['05. price']),
        'change': float(data['Global Quote']['09. change']),
        'change_percent': data['Global Quote']['10. change percent']
    }

def get_stock_data(symbol):
    """Fetch the historical stock data for a given symbol."""
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={Config.FMP_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['historical'][:30]  # Return last 30 days of data
