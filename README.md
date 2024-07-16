# Stock Portfolio Tracker

Stock Portfolio Tracker is a web application that allows users to manage their stock portfolios, track stock prices, and view historical stock data.

## Features

- User registration and authentication
- Dashboard to view current portfolio
- Add and remove stocks from the portfolio
- View stock quotes and historical data
- Interactive charts to visualize stock performance

## Technologies Used

- Frontend: HTML5, Bootstrap 5, JavaScript (vanilla), Chart.js
- Backend: Flask, SQLAlchemy, Flask-Login
- Database: SQLite (can be upgraded to PostgreSQL)
- APIs: Alpha Vantage, Financial Modeling Prep

## Project Structure

```plaintext
StockPortfolioTracker/
├── Portfolio_Tracker/
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── stock_data.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── add_stock.html
├── config.py
├── run.py
└── README.md
