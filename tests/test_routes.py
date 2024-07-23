import unittest
from app import app, db
from models import User

class RoutesTestCase(unittest.TestCase):
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
        test_user = User(username='jtest', email='jtest@example.com')
        test_user.set_password('password')
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
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign up or log in to get started.', response.data)  

    def test_login_get(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data)

    def test_login_post(self):
        response = self.client.post('/login', data=dict(
            username='jtest',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username', response.data)  

    def test_invalid_login_post(self):
        response = self.client.post('/login', data=dict(
            username='notjohn',
            password='notpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'value="notjohn"', response.data)

    def test_logout(self):
        self.client.post('/login', data=dict(
            username='jtest',
            password='password'
        ), follow_redirects=True)
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign up or log in to get started.', response.data)  

    def test_register_get(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_register_post(self):
        response = self.client.post('/register', data=dict(
            username='jtest',
            email='jtest@example.com',
            password='password',
            password2='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'value="Register"', response.data)


if __name__ == '__main__':
    unittest.main()
