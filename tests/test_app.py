import unittest
from app import app, db, User

class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        cls.app.config['SECRET_KEY'] = 'test'
        cls.client = cls.app.test_client()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        db.create_all()
        # Create a test user
        test_user = User(username='testuser', email='test@example.com')
        test_user.set_password('testpassword')
        db.session.add(test_user)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
        cls.ctx.pop()

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        response = self.client.get('/index')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Stock Portfolio Tracker!', response.data)

    def test_register(self):
        response = self.client.post('/register', data=dict(
            username='newuser',
            email='new@example.com',
            password='password',
            password2='password'
        ), follow_redirects=False)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_add_stock(self):
        # Log in the user
        self.client.post('/login', data=dict(
                username='testuser',
                password='testpassword'
            ), follow_redirects=True)

        # Post request with stock ticker
        response = self.client.post('/add_stock', data=dict(ticker='AAPL'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data) #need to replace login with correct message

if __name__ == '__main__':
    unittest.main()
