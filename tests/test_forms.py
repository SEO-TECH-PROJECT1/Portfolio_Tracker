import unittest
from app import app, db
from forms import RegistrationForm
from models import User

class RegistrationFormTestCase(unittest.TestCase):
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

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
        cls.ctx.pop()

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()

        # clear db before tests
        db.session.remove()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        self.app_context.pop()

    def test_validate_username(self):
        # Create a user with the username 'existinguser'
        user = User(username='jtest', email='jtest@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        # Create a registration form with the same username
        with self.app.test_request_context():
            form = RegistrationForm(username='jtest', email='jtest@example.com',
                                    password='password', password2='password')
            # Check if form validation fails with the existing username
            self.assertFalse(form.validate())
            self.assertIn('Please use a different username.', form.errors['username'])

    def test_validate_email(self):
        # Create a user with the email 'existing@example.com'
        user = User(username='johnnytest', email='johnny@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        # Create a registration form with the same email
        with self.app.test_request_context():
            form = RegistrationForm(username='johnnytest', email='johnny@example.com',
                                    password='password', password2='password')
            # Check if form validation fails with the existing email
            self.assertFalse(form.validate())
            self.assertIn('Please use a different email address.', form.errors['email'])

if __name__ == '__main__':
    unittest.main()
