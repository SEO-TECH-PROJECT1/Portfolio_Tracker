# app.py

import git
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import matplotlib.pyplot as plt
import io
import base64
import random
from datetime import datetime, timedelta
import requests


# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///stock_portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ALPHA_VANTAGE_API_KEY'] = os.environ.get('ALPHA_VANTAGE_API_KEY') or 'your_api_key_here'

# Print all config keys to the terminal
print("Configuration Keys:")
for key in app.config:
    print(f"{key}: {app.config[key]}")

# Extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Logging setup
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/portfolio_tracker.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Portfolio Tracker startup')

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class StockForm(FlaskForm):
    ticker = StringField('Ticker', validators=[DataRequired()])
    submit = SubmitField('Add Stock')

# Routes
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('dashboard'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    # Mock data for demonstration
    stocks = {
        '2024-07-18': {'symbol': 'AAPL', 'price': '150.00'},
        '2024-07-19': {'symbol': 'GOOGL', 'price': '2800.00'},
        '2024-07-20': {'symbol': 'AMZN', 'price': '3400.00'}
    }
    return render_template('dashboard.html', title='Dashboard', stocks=stocks)

@app.route('/profile')
@login_required
def profile():
    profile_info = {
        'username': current_user.username,
        'email': current_user.email,
        'joined': '2023-01-01',
        'preferred_stocks': ['AAPL', 'GOOGL', 'TSLA']
    }
    return render_template('profile.html', title='Profile', profile_info=profile_info)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.profile_picture = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_picture)
    return render_template('account.html', title='Account', profile_image=profile_image, form=form)

@app.route('/stock_tracker')
@login_required
def stock_tracker():
    # Mock data for demonstration
    stocks = {
        '2024-07-18': {'symbol': 'AAPL', 'price': '150.00'},
        '2024-07-19': {'symbol': 'GOOGL', 'price': '2800.00'},
        '2024-07-20': {'symbol': 'AMZN', 'price': '3400.00'}
    }
    return render_template('stock_tracker.html', title='Stock Tracker', stocks=stocks)


@app.route('/recommendations')
@login_required
def recommendations():
    recommendations = get_mock_recommendations()  # Replace with actual recommendation logic
    return render_template('recommendations.html', title='Recommendations', recommendations=recommendations)

@app.route('/intraday/<ticker>', methods=['GET', 'POST'])
@login_required
def intraday(ticker):
    interval = request.args.get('interval', '5min')
    outputsize = request.args.get('outputsize', 'compact')
    stock_data, is_api_data = get_stock_data(ticker, function='TIME_SERIES_INTRADAY', interval=interval, outputsize=outputsize)
    graph_url = create_stock_graph(ticker, stock_data) if stock_data else None
    return render_template('intraday.html', title=f'Intraday Data for {ticker}', ticker=ticker, stock_data=stock_data, graph_url=graph_url, is_api_data=is_api_data)

# Error handling
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Stock Data with error handling and mock data fallback
def get_stock_data(ticker, function='TIME_SERIES_DAILY', interval='5min', outputsize='compact', adjusted=True, extended_hours=True, month=None):
    api_key = app.config['ALPHA_VANTAGE_API_KEY']
    base_url = 'https://www.alphavantage.co/query?'
    params = {
        'function': function,
        'symbol': ticker,
        'apikey': api_key,
    }

    if function == 'TIME_SERIES_INTRADAY':
        params['interval'] = interval
        params['outputsize'] = outputsize
        params['adjusted'] = 'true' if adjusted else 'false'
        params['extended_hours'] = 'true' if extended_hours else 'false'
        if month:
            params['month'] = month

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'Error Message' in data:
            app.logger.error(f"Error retrieving data for {ticker}")
            return get_mock_stock_data(ticker), False

        if function == 'TIME_SERIES_INTRADAY':
            time_series_key = f"Time Series ({interval})"
        else:
            time_series_key = 'Time Series (Daily)'

        time_series = data.get(time_series_key)
        if not time_series:
            return get_mock_stock_data(ticker), False

        return time_series, True

    except requests.RequestException as e:
        app.logger.error(f"Request failed for {ticker}: {e}")
        return get_mock_stock_data(ticker), False

def get_mock_stock_data(ticker):
    app.logger.info(f"Returning mock data for {ticker}")
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
        {'ticker': 'TSLA', 'recommendation': 'Hold'},
        {'ticker': 'GOOGL', 'recommendation': 'Sell'},
    ]

# Dynamic graph creation
def create_stock_graph(ticker, time_series):
    dates = list(time_series.keys())
    close_prices = [float(time_series[date]['4. close']) for date in dates]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, close_prices, marker='o', linestyle='-', color='b')
    plt.title(f'Stock Prices for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return f'data:image/png;base64,{graph_url}'

#deployment function
@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/PortfolioTracker/Portfolio_Tracker')
        origin = repo.remotes.origin
        origin.pull('branch_4_BR_02')
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
        
if __name__ == '__main__':
    app.run(debug=True)
