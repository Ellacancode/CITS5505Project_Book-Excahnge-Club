import unittest  
from flask import url_for 
from flask_testing import TestCase  
from Bookclub import create_app, db, bcrypt  
from Bookclub.models import User # Import the User model from the Bookclub module

class UserProfilePageTestCase(TestCase):  

    def create_app(self): 
        app = create_app('testing')  
        return app  

    def setUp(self):  # Method that runs before each test
        self.client = self.app.test_client() 
        with self.app.app_context(): 
            db.create_all()  
            self.hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')  # Generate a hashed password
            self.user = User(username='existinguser', email='existingemail@gmail.com', password=self.hashed_password)  # Create a User instance
            db.session.add(self.user)  # Add the user to the session
            db.session.commit()  # Commit the session to save the user to the database

    def tearDown(self):  # Method that runs after each test
        with self.app.app_context(): 
            db.session.remove()  # Remove the database session to prevent the session from being used in the next test

    def login(self, email='existingemail@gmail.com', password='password'):  # Method to log in a user
        return self.client.post(url_for('main.login'), data=dict(
            email=email,
            password=password
        ), follow_redirects=True)  # Post login data and follow redirects

    def test_user_profile_page(self):  # Define a test method for the user profile page
        self.login()  # Log in the user
        response = self.client.get(url_for('main.user', username='existinguser'))  # Send a GET request to the user profile page
        self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200
        self.assertIn(b'existinguser', response.data)  # Assert that the response data contains the username

if __name__ == '__main__':  # If this script is run as the main program
    unittest.main()  # Run the unit tests

