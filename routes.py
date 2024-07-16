# File: Portfolio_Tracker/routes.py
# Description: Define the routes and views for the Flask application.

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, Portfolio, Stock
from app.forms import LoginForm, RegistrationForm, AddStockForm
from app.stock_data import get_stock_data, get_stock_quote

@app.route('/')
@app.route('/index')
def index():
    """Render the home page."""
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
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
    """Handle user logout."""
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle new user registration."""
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
    """Display the user dashboard with portfolio summary."""
    portfolio = current_user.portfolios.first()
    if portfolio is None:
        portfolio = Portfolio(name='Default', user=current_user)
        db.session.add(portfolio)
        db.session.commit()
    stocks = portfolio.stocks.all()
    stock_data = [get_stock_quote(stock.symbol) for stock in stocks]
    return render_template('dashboard.html', title='Dashboard', stocks=stock_data)

@app.route('/add_stock', methods=['GET', 'POST'])
@login_required
def add_stock():
    """Add a stock to the user's portfolio."""
    form = AddStockForm()
    if form.validate_on_submit():
        portfolio = current_user.portfolios.first()
        stock = Stock(symbol=form.symbol.data, shares=form.shares.data, purchase_price=form.purchase_price.data, portfolio=portfolio)
        db.session.add(stock)
        db.session.commit()
        flash(f'Added {form.shares.data} shares of {form.symbol.data} to your portfolio.')
        return redirect(url_for('dashboard'))
    return render_template('add_stock.html', title='Add Stock', form=form)

@app.route('/remove_stock/<int:stock_id>', methods=['POST'])
@login_required
def remove_stock(stock_id):
    """Remove a stock from the user's portfolio."""
    stock = Stock.query.get_or_404(stock_id)
    if stock.portfolio.user != current_user:
        flash('You do not have permission to remove this stock.')
        return redirect(url_for('dashboard'))
    db.session.delete(stock)
    db.session.commit()
    flash(f'Removed {stock.symbol} from your portfolio.')
    return redirect(url_for('dashboard'))

@app.route('/stock_data/<symbol>')
@login_required
def stock_data(symbol):
    """Fetch and return stock data as JSON."""
    data = get_stock_data(symbol)
    return jsonify(data)
