# File: Portfolio_Tracker/stock_data.py
# Description: Module for fetching stock data from external APIs.


import requests
from pprint import pprint

MA_API_KEY = ""
AV_API_KEY = ""


# def get_stock_quote(symbol):
#     """Fetch the current stock quote for a given symbol."""
#     url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={Config.ALPHA_VANTAGE_API_KEY}'
#     response = requests.get(url)
#     data = response.json()
#     return {
#         'symbol': symbol,
#         'price': float(data['Global Quote']['05. price']),
#         'change': float(data['Global Quote']['09. change']),
#         'change_percent': data['Global Quote']['10. change percent']
#     }

# def get_stock_data(symbol):
#     """Fetch the historical stock data for a given symbol."""
#     url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={Config.FMP_API_KEY}'
#     response = requests.get(url)
#     data = response.json()
#     return data['historical'][:30]  # Return last 30 days of data

def get_weekly_stock_data(symbol):
    """Fetch the weekly stock data for a given symbol."""
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={symbol}&apikey={AV_API_KEY}'
    response = requests.get(url)
    data = response.json()

def get_stock_news(symbol):
    """Fetch the latest news articles for a given stock symbol."""
    url = f'https://api.marketaux.com/v1/news/all?symbols={symbol}&filter_entities=true&language=en&api_token={MA_API_KEY}&limit=3'
    response = requests.get(url)
    data = response.json()
    return data


# pprint(get_stock_news("AAPL"))  
#pprint(get_weekly_stock_data("AAPL"))




