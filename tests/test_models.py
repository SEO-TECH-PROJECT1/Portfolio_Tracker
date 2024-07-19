import unittest
from app import app, db
from models import User, Stock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app
        self.client = app.test_client()

        engine = create_engine('sqlite:///:memory:')
        db.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()

    def test_password_hashing(self):
        u = User(username='johnnytest', email='jtest@example.com')
        u.set_password('password123')
        self.assertTrue(u.check_password('password123'))
        self.assertFalse(u.check_password('notpassword'))

    def test_user_creation(self):
        u = User(username='johnnytest', email='jtest@example.com')
        u.set_password('password123')
        self.session.add(u)
        self.session.commit()
        self.assertEqual(self.session.query(User).count(), 1)
        self.assertEqual(self.session.query(User).first().username, 'johnnytest')

class StockModelCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app
        self.client = app.test_client()

        engine = create_engine('sqlite:///:memory:')
        db.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()

    def test_stock_creation(self):
        u = User(username='johnnytest', email='jtest@example.com')
        u.set_password('password123')
        self.session.add(u)
        self.session.commit()

        s = Stock(ticker='GOOGL', user_id=u.id)
        self.session.add(s)
        self.session.commit()

        self.assertEqual(self.session.query(Stock).count(), 1)
        self.assertEqual(self.session.query(Stock).first().ticker, 'GOOGL')

if __name__ == '__main__':
    unittest.main()
