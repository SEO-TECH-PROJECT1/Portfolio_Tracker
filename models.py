# File: Portfolio_Tracker/models.py
# Description: Define the database models for the application.

from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """User model to store user information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    portfolios = db.relationship('Portfolio', backref='user', lazy='dynamic')

    def set_password(self, password):
        """Generate password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

class Portfolio(db.Model):
    """Portfolio model to manage user's stock portfolio."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    stocks = db.relationship('Stock', backref='portfolio', lazy='dynamic')

class Stock(db.Model):
    """Stock model to store stock information."""
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10))
    shares = db.Column(db.Integer)
    purchase_price = db.Column(db.Float)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))

@login_manager.user_loader
def load_user(id):
    """Load user by ID."""
    return User.query.get(int(id))
