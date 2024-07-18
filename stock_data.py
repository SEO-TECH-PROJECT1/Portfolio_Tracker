# File: Portfolio_Tracker/stock_data.py
# Description: Module for fetching stock data from external APIs.

import requests
from flask import current_app
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def get_stock_data(ticker):
    api_key = current_app.config['ALPHA_VANTAGE_API_KEY']
    base_url = 'https://www.alphavantage.co/query?'
    function = 'TIME_SERIES_DAILY'
    url = f'{base_url}function={function}&symbol={ticker}&apikey={api_key}'
    try:
        response = requests.get(url)
        data = response.json()
        if 'Error Message' in data:
            raise ValueError("API Error")
        time_series = data.get('Time Series (Daily)')
        if not time_series:
            raise ValueError("Invalid Data")
        return time_series
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return generate_mock_data(ticker)

def generate_mock_data(ticker):
    end_date = datetime.now()
    mock_data = {}
    for i in range(30):
        date_str = (end_date - timedelta(days=i)).strftime('%Y-%m-%d')
        mock_data[date_str] = {
            '1. open': str(random.uniform(100, 500)),
            '2. high': str(random.uniform(100, 500)),
            '3. low': str(random.uniform(100, 500)),
            '4. close': str(random.uniform(100, 500)),
            '5. volume': str(random.randint(1000, 10000))
        }
    return mock_data

def create_stock_chart(stock_data):
    dates = list(stock_data.keys())
    closes = [float(stock_data[date]['4. close']) for date in dates]
    plt.figure(figsize=(10, 5))
    plt.plot(dates, closes, label='Close Price')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Stock Price Over Last 30 Days')
    plt.legend()
    plt.grid(True)
    chart_path = 'static/stock_chart.png'
    plt.savefig(chart_path)
    plt.close()
    return chart_path
