# data.py


import random
from datetime import datetime, timedelta

def get_mock_stock_data(ticker):
    mock_data = {}
    for i in range(30):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')
        mock_data[date] = {
            '1. open': f"{random.uniform(100, 500):.2f}",
            '2. high': f"{random.uniform(100, 500):.2f}",
            '3. low': f"{random.uniform(100, 500):.2f}",
            '4. close': f"{random.uniform(100, 500):.2f}",
            '5. volume': f"{random.randint(100000, 5000000)}"
        }
    return mock_data

def get_mock_recommendations():
    return [
        {'ticker': 'AAPL', 'recommendation': 'Buy'},
        {'ticker': 'GOOGL', 'recommendation': 'Hold'},
        {'ticker': 'TSLA', 'recommendation': 'Sell'},
        {'ticker': 'AMZN', 'recommendation': 'Buy'},
        {'ticker': 'MSFT', 'recommendation': 'Hold'}
    ]

def get_mock_profile(user):
    return {
        'username': user.username,
        'email': user.email,
        'joined': '2023-01-01',
        'preferred_stocks': ['AAPL', 'GOOGL', 'TSLA']
    }
