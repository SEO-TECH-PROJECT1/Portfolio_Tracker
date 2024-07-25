# File: Portfolio_Tracker/routes.py
# Description: Define the routes and views for the Flask application.

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from Portfolio_Tracker import db
from Portfolio_Tracker.models import User
from Portfolio_Tracker.forms import LoginForm, RegistrationForm, StockForm


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@bp.route('/view_stocks')
@login_required
def view_stocks():
    stocks = Stock.query.filter_by(user_id=current_user.id).all()
    return render_template('view_stocks.html', stocks=stocks)

@bp.route('/add_stock', methods=['GET', 'POST'])
@login_required
def add_stock():
    form = StockForm()
    if form.validate_on_submit():
        stock = Stock(
            ticker=form.ticker.data,
            quantity=form.quantity.data,
            purchase_price=form.purchase_price.data,
            user_id=current_user.id
        )
        db.session.add(stock)
        db.session.commit()
        flash('Stock added successfully!')
        return redirect(url_for('main.view_stocks'))
    return render_template('add_stock.html', form=form)

