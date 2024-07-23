import unittest
from flask import Flask
from stock_data import get_stock_data
from dotenv import load_dotenv
import os
from datetime import datetime


class StockDataTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load environment variables from .env file
        load_dotenv()

    def setUp(self):
        self.ticker = 'AAPL'

        # Create a test app and context
        self.app = Flask(__name__)
        self.app.config['ALPHA_VANTAGE_API_KEY'] = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_get_stock_data(self):
        data = get_stock_data(self.ticker)
        self.assertIsNotNone(data)

        current_year = datetime.now().strftime('%Y') #Check if current year in data
        years_check = {date[:4] for date in data.keys()}
        self.assertIn(current_year, years_check)

    def test_get_stock_data_invalid(self):
        invalid_ticker = 'NOTVALID'
        data = get_stock_data(invalid_ticker)
        self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()
