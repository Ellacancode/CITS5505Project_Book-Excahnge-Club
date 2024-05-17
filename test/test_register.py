# This test suite test the registration page functionality 
import unittest
from flask import url_for
from flask_testing import TestCase
from Bookclub import create_app, db
from Bookclub.models import User

class RegisterPageTestCase(TestCase):

    def create_app(self):
        # Create the app with testing configuration
        app = create_app('testing')
        return app

    def setUp(self):
        # Set up the test client and initialize the database
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Add a test user with a unique username and email
            user = User(username='testuser', email='testuser@example.com', password='Password1!')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        # Tear down the database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_page_get(self):
        # Test GET request to the register page
        response = self.client.get(url_for('main.register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Join a Community of Readers', response.data)

    def test_register_page_post_success(self):
        # Test successful POST request to the register page
        response = self.client.post(url_for('main.register'), data=dict(
            username='newuser',
            email='newuser@example.com',
            password='Password1!',
            confirm_password='Password1!'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created!', response.data)

    def test_register_page_post_existing_username(self):
        # Test POST request with an existing username
        response = self.client.post(url_for('main.register'), data=dict(
            username='testuser',
            email='newemail@example.com',
            password='Password1!',
            confirm_password='Password1!'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sorry, the username is unavailable, please choose another one.', response.data)

    def test_register_page_post_existing_email(self):
        # Test POST request with an existing email
        response = self.client.post(url_for('main.register'), data=dict(
            username='newusername',
            email='testuser@example.com',
            password='Password1!',
            confirm_password='Password1!'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sorry, the email is unavailable, please choose a different one.', response.data)

    def test_register_page_post_password_mismatch(self):
        # Test POST request with mismatched passwords
        response = self.client.post(url_for('main.register'), data=dict(
            username='newuser',
            email='newuser@example.com',
            password='Password1!',
            confirm_password='Password2!'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords must match', response.data)

    def test_register_page_post_invalid_password(self):
        # Test POST request with an invalid password
        response = self.client.post(url_for('main.register'), data=dict(
            username='newuser',
            email='newuser@example.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character', response.data)

if __name__ == '__main__':
    unittest.main()


