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
```

## Project Files Overview

### 1. Application Initialization (`__init__.py`)
This file initializes the Flask application and configures extensions.

- **Location**: `Portfolio_Tracker/__init__.py`
- **Description**: Initialize the Flask application and configure extensions.
- **Analysis**: This file sets up the Flask app, SQLAlchemy, and Flask-Login extensions. It also imports the routes and models modules.

### 2. Configuration (`config.py`)
This file loads the configuration for the Flask application, including environment variables.

- **Location**: `Portfolio_Tracker/config.py`
- **Description**: Configuration file for the Flask application.
- **Analysis**: This file uses `dotenv` to load environment variables and sets configuration options such as the secret key and database URI.

### 3. Stock Data (`stock_data.py`)
This file fetches stock data from external APIs.

- **Location**: `Portfolio_Tracker/stock_data.py`
- **Description**: Module for fetching stock data from external APIs.
- **Analysis**: This file includes functions to fetch current stock quotes from Alpha Vantage and historical stock data from Financial Modeling Prep.

### 4. Models (`models.py`)
This file defines the database models for the application.

- **Location**: `Portfolio_Tracker/models.py`
- **Description**: Define the database models for the application.
- **Analysis**: This file defines the `User`, `Portfolio`, and `Stock` models using SQLAlchemy. It includes methods for setting and checking passwords and sets up relationships between models.

### 5. Forms (`forms.py`)
This file defines the web forms used in the application.

- **Location**: `Portfolio_Tracker/forms.py`
- **Description**: Define the web forms used in the application.
- **Analysis**: This file includes forms for user login, registration, and adding stocks. It uses Flask-WTF for form handling and validation.

### 6. Routes (`routes.py`)
This file defines the routes and views for the Flask application.

- **Location**: `Portfolio_Tracker/routes.py`
- **Description**: Define the routes and views for the Flask application.
- **Analysis**: This file sets up the routes for the home page, user login, logout, registration, dashboard, adding stocks, removing stocks, and fetching stock data. It uses Flask-Login to protect certain routes and manage user sessions.

### Summary
Each of these files is essential for the functionality of the Flask application. They are properly set up and interlinked to ensure the smooth operation of the application. The `__init__.py` file initializes the app, `config.py` loads the configuration, `stock_data.py` fetches stock data, `models.py` defines the database models, `forms.py` handles form validation, and `routes.py` defines the application routes.


## Template Files Overview

### 1. Base Template (`base.html`)
This template sets up the common HTML structure that is extended by other templates. It includes the navigation bar and the basic layout structure.

- **Location**: `Portfolio_Tracker/templates/base.html`
- **Description**: Base template for the application with common layout and styles.
- **Analysis**: This file is correctly set up with Bootstrap for styling and contains a dynamic block for the title and content. Navigation links adjust based on the user's authentication status.

### 2. Home Page (`index.html`)
This template provides the landing page for your application.

- **Location**: `Portfolio_Tracker/templates/index.html`
- **Description**: Template for the home page.
- **Analysis**: It extends the base template and includes a welcoming message with buttons to either log in or register.

### 3. Login Page (`login.html`)
This template is used for the user login form.

- **Location**: `Portfolio_Tracker/templates/login.html`
- **Description**: Template for the login page.
- **Analysis**: It includes form handling for username, password, and a remember me option, extending the base template to utilize common styles and scripts.

### 4. Registration Page (`register.html`)
This template is used for new user registrations.

- **Location**: `Portfolio_Tracker/templates/register.html`
- **Description**: Template for the registration page.
- **Analysis**: It extends the base template and includes form fields for username, email, password, and password confirmation.

### 5. Dashboard Page (`dashboard.html`)
This template displays the user's stock portfolio.

- **Location**: `Portfolio_Tracker/templates/dashboard.html`
- **Description**: Template for displaying the user's stock portfolio dashboard.
- **Analysis**: It extends the base template and includes a section for portfolio summary and a graph. It also dynamically lists stocks with their current prices and provides an option to add more stocks.

### 6. Add Stock Page (`add_stock.html`)
This template allows users to add stocks to their portfolio.

- **Location**: `Portfolio_Tracker/templates/add_stock.html`
- **Description**: Template for the add stock page.
- **Analysis**: It includes form fields for stock symbol, number of shares, and purchase price. Extends the base template for consistent layout.

### Summary
Each of these templates is properly linked with the `base.html` for consistent styling and navigation. They also utilize Flask's templating features such as `url_for` for routing and `{{ form.hidden_tag() }}` for CSRF protection in forms.


## Running the Application

1. Set up the virtual environment and install dependencies:
```plaintext
   sh
   python3 -m venv venv
   source venv/bin/activate # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
```

3. Set up environment variables:
   Ensure you have a .env file in the root directory with the following content:
  
```plaintext
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
   FMP_API_KEY=your_fmp_api_key
   SECRET_KEY=your_secret_key
```

4. Initialize the database:
```plaintext
   sh
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
```

5. Run the application:
```plaintext
   sh
   set FLASK_APP=run.py
   flask run
```
