# File: Portfolio_Tracker/stock_data.py
# Description: Module for fetching stock data from external APIs.


import requests
from pprint import pprint
import mock
from datetime import datetime, timedelta

# MA_API_KEY = ""
# AV_API_KEY = ""





def get_weekly_stock_data(symbol):
    """Fetch the weekly stock data for a given symbol."""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={symbol}&apikey={AV_API_KEY}&outputsize=compact&datatype=json&interval=weekly&from={start_date}&to={end_date}'
    response = requests.get(url)
    data = response.json()
    if data != None:
        return data
    return mock.data

def get_stock_news(symbol):
    """Fetch the latest news articles for a given stock symbol."""
    url = f'https://api.marketaux.com/v1/news/all?symbols={symbol}&filter_entities=true&language=en&api_token={MA_API_KEY}&limit=3'
    response = requests.get(url)
    data = response.json()
    return data


def get_last_week(data):
    time_series = data["Weekly Adjusted Time Series"]
    last_7_entries = list(time_series.keys())[:8]
    return {date: time_series[date] for date in last_7_entries}









