from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import re
import os
import google.generativeai as genai

from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv("AI_API"))
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '542518875d279e44e674875bd5dc4847c61fe744497fd33c'  # Replace with your generated key

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

def fetch_stock_data(symbol):
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def is_valid_stock_symbol(symbol):
    data = fetch_stock_data(symbol)
    return 'Error Message' not in data

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if 'register' in request.form:
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
            else:
                user = User(username=username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash('Registration successful, please log in.')
        elif 'login' in request.form:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                return redirect(url_for('portfolio'))
            else:
                flash('Invalid username or password')
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    if 'user_id' not in session:
        flash('You need to be logged in to view your portfolio.')
        return redirect(url_for('index'))

    if request.method == 'POST':
        symbol = request.form['symbol'].strip().upper()
        if is_valid_stock_symbol(symbol):
            user_id = session['user_id']
            if not Stock.query.filter_by(symbol=symbol, user_id=user_id).first():
                stock = Stock(symbol=symbol, user_id=user_id)
                db.session.add(stock)
                db.session.commit()
                flash('Stock added to your portfolio')
            else:
                flash('Stock symbol already in your portfolio')
        else:
            flash('Invalid stock symbol')
        return redirect(url_for('portfolio'))

    user_id = session['user_id']
    stocks = Stock.query.filter_by(user_id=user_id).all()
    return render_template('portfolio.html', stocks=stocks)

@app.route('/stock/<symbol>', methods=['GET'])
def stock_details(symbol):
    data = fetch_stock_data(symbol)
    if 'Error Message' in data:
        flash('Invalid stock symbol')
        return redirect(url_for('portfolio'))
    
    time_series = data.get('Time Series (1min)', {})
    latest_time = next(iter(time_series), None)
    stock_info = time_series.get(latest_time, {}) if latest_time else {}
    
    return render_template('stock_details.html', symbol=symbol, info=stock_info)

@app.route('/remove_stock/<int:stock_id>', methods=['POST'])
def remove_stock(stock_id):
    stock = Stock.query.get_or_404(stock_id)
    if stock.user_id != session['user_id']:
        flash('Unauthorized action')
        return redirect(url_for('portfolio'))
    
    db.session.delete(stock)
    db.session.commit()
    flash('Stock removed from your portfolio')
    return redirect(url_for('portfolio'))

@app.route('/search', methods=['POST'])
def search():
    symbol = request.form['symbol'].strip().upper()
    if is_valid_stock_symbol(symbol):
        return redirect(url_for('stock_details', symbol=symbol))
    else:
        flash('Invalid stock symbol')
        return redirect(url_for('portfolio'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('You need to be logged in to access your profile.')
        return redirect(url_for('index'))

    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        if new_username:
            user.username = new_username
        if new_password:
            user.set_password(new_password)
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful, please log in.')
            return redirect(url_for('index'))
    return render_template('register.html')


from flask import jsonify
from chatbot import get_bot_response


def generate_response_with_role(message):
    # Define the role for the chatbot
    role_prompt = ("You are a concise and knowledgeable stock advisor. "
        "Provide brief, specific, and actionable responses to stock-related questions. "
        "If asked about current market conditions, give a direct answer based on general knowledge or common factors affecting the market. "
        "If the question requires current data, acknowledge that and suggest checking recent news or financial sources. Do not use markdown.")
    prompt = f"{role_prompt}\n\nUser: {message}\n\nChatBot:"
    response = model.generate_content(prompt)
    return response.text.strip()

@app.route('/chat', methods=['POST'])
def chat():
    message = request.form['message']
    response_text = generate_response_with_role(message)
    return jsonify({'response': response_text})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)

