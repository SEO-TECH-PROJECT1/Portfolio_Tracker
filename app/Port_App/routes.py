# routes.py (update)
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Stock, Friendship
from config import Config
import requests
import os

bp = Blueprint('routes', __name__)
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Attempting login with username: {username}, password: {password}")  # Debugging line
        
        if 'register' in request.form:
            # Register a new user
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
            else:
                user = User(username=username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash('Registration successful, please log in.')
        elif 'login' in request.form:
            # Login an existing user
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                # Handle login success
                flash('Login successful')
                session['user_id'] = user.id  # Store user ID in session
                return redirect(url_for('routes.portfolio'))
            else:
                flash('Invalid username or password')
        return redirect(url_for('routes.index'))
    return render_template('index.html')




@bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if User.query.filter_by(username=username).first():
        flash('Username already exists')
    else:
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful, please log in.')
    return redirect(url_for('routes.index'))

@bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Handle login success (e.g., set session, redirect)
        flash('Login successful')
    else:
        flash('Invalid username or password')
    return redirect(url_for('routes.index'))

@bp.route('/add_friends', methods=['GET', 'POST'])
def add_friends():
    if request.method == 'POST':
        friend_id = request.form['friend_id']
        user_id = 1  # Assume user is logged in

        if user_id == int(friend_id):
            flash('You cannot add yourself as a friend')
            return redirect(url_for('routes.add_friends'))

        existing_friendship = Friendship.query.filter_by(user_id=user_id, friend_id=friend_id).first()
        if existing_friendship:
            flash('Friendship already exists')
        else:
            friendship = Friendship(user_id=user_id, friend_id=friend_id)
            db.session.add(friendship)
            db.session.commit()
            flash('Friend added successfully')
        return redirect(url_for('routes.add_friends'))

    users = User.query.all()
    return render_template('add_friends.html', users=users)


def fetch_stock_data(symbol):
    api_key = Config.ALPHA_VANTAGE_API_KEY
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


@bp.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    if 'user_id' not in session:
        flash('You need to be logged in to view your portfolio.')
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        symbol = request.form['symbol']
        stock_data = fetch_stock_data(symbol)
        if 'Error Message' in stock_data:
            flash('Invalid stock symbol or API error.')
        else:
            user_id = session['user_id']
            stock = Stock(symbol=symbol, user_id=user_id)
            db.session.add(stock)
            db.session.commit()
            flash('Stock added to your portfolio')
        return redirect(url_for('routes.portfolio'))

    user_id = session['user_id']
    stocks = Stock.query.filter_by(user_id=user_id).all()
    return render_template('portfolio.html', stocks=stocks)


@bp.route('/stock_history/<symbol>', methods=['GET'])
def stock_history(symbol):
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'Error Message' in data:
        flash('Invalid stock symbol')
        return redirect(url_for('routes.portfolio'))

    time_series = data.get('Time Series (Daily)', {})
    dates = list(time_series.keys())
    prices = [float(time_series[date]['4. close']) for date in dates]

    return render_template('stock_history.html', symbol=symbol, dates=dates, prices=prices)