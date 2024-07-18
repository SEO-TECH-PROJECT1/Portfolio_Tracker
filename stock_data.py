# File: Portfolio_Tracker/stock_data.py
# Description: Module for fetching stock data from external APIs.

import requests
from flask import current_app

def get_stock_data(ticker):
    api_key = current_app.config['ALPHA_VANTAGE_API_KEY']
    base_url = 'https://www.alphavantage.co/query?'
    function = 'TIME_SERIES_DAILY'
    url = f'{base_url}function={function}&symbol={ticker}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    
    if 'Error Message' in data:
        return None
    
    time_series = data.get('Time Series (Daily)')
    if not time_series:
        return None
    
    return time_series
