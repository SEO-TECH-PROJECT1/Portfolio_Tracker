# app.py

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import requests
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Flask application setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///stock_portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticker = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)

# Forms
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
    ticker = StringField('Stock Ticker', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    purchase_price = StringField('Purchase Price', validators=[DataRequired()])
    submit = SubmitField('Add Stock')

# Routes
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
    stocks = Stock.query.filter_by(user_id=current_user.id).all()
    for stock in stocks:
        stock_data = get_stock_data(stock.ticker)
        stock.chart_path = create_stock_chart(stock_data)
    return render_template('dashboard.html', stocks=stocks)

@app.route('/profile')
@login_required
def profile():
    user = User.query.get_or_404(current_user.id)
    stocks = Stock.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', user=user, stocks=stocks)

@app.route('/stock_tracker')
@login_required
def stock_tracker():
    stocks = Stock.query.filter_by(user_id=current_user.id).all()
    stock_data = {}
    for stock in stocks:
        data = get_stock_data(stock.ticker)
        stock_data[stock.ticker] = data
    chart_path = create_stock_chart(stock_data)
    return render_template('stock_tracker.html', stocks=stocks, chart_path=chart_path)

@app.route('/recommendations')
@login_required
def recommendations():
    recommendations = [
        {'ticker': 'AAPL', 'current_price': 150.00, 'recommendation': 'Buy', 'reason': 'Strong growth potential'},
        {'ticker': 'GOOGL', 'current_price': 2800.00, 'recommendation': 'Hold', 'reason': 'Stable performance'},
        {'ticker': 'TSLA', 'current_price': 700.00, 'recommendation': 'Sell', 'reason': 'Overvalued'}
    ]
    return render_template('recommendations.html', recommendations=recommendations)

# Stock Data functions
def get_stock_data(ticker):
    api_key = app.config['ALPHA_VANTAGE_API_KEY']
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

if __name__ == "__main__":
    app.run(debug=True)
