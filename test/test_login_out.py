import unittest  # Import the unittest module for creating unit tests
from flask import url_for  # Import url_for to build URLs for the application
from Bookclub import create_app, db, bcrypt  # Import necessary components from the Bookclub module
from Bookclub.models import User  # Import the User model from the models module

# Purpose: To verify login and logout functionality
class UserAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')  # Create the Flask application with the 'testing' configuration
        self.app_context = self.app.app_context()  # Create an application context
        self.app_context.push()  # Push the application context
        db.create_all()  # Create all database tables
        self.client = self.app.test_client()  # Create a test client for the app

        # Create and add a user to the database
        self.hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        self.user = User(username='testuser', email='testuser@example.com', password=self.hashed_password)
        db.session.add(self.user)
        db.session.commit()  # Commit the changes

    def tearDown(self):
        db.session.remove()  # Remove the database session
        db.drop_all()  # Drop all database tables
        self.app_context.pop()  # Pop the application context

    def login(self, email='testuser@example.com', password='password'):
        return self.client.post(url_for('main.login'), data=dict(
            email=email,
            password=password
        ), follow_redirects=True)  # Submit login data and follow redirects

    def logout(self):
        return self.client.get(url_for('main.logout'), follow_redirects=True)  # Send a GET request to log out

    def test_login_page(self):
        with self.app.test_request_context():
            # Test the login page rendering
            response = self.client.get(url_for('main.login'))
            self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200
            self.assertIn(b'Log In', response.data)  # Assert that the response data contains 'Log In'

            # Test the login functionality
            response = self.login(email='testuser@example.com', password='password')
            self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200
            self.assertIn(b'Home', response.data)  # Assert that the response data contains 'Home'

    def test_logout(self):
        with self.app.test_request_context():
            # Test the logout functionality
            self.login(email='testuser@example.com', password='password')  # Log in first
            response = self.logout()  # Attempt to log out
            self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200
            self.assertIn(b'Home', response.data)  # Assert that the response data contains 'Home'

if __name__ == '__main__':
    unittest.main()  # Run the unit tests if this script is executed directly




