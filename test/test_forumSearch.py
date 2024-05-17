import unittest  # Import the unittest module for creating unit tests
from flask import url_for  
from Bookclub import create_app, db, bcrypt  
from Bookclub.models import User, Post  # Import the User and Post models

# Purpose: To verify the search functionality
class SearchFunctionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')  # Create the Flask application with the 'testing' configuration
        self.app_context = self.app.app_context()  # Create an application context
        self.app_context.push() 
        db.create_all()  # Create all database tables
        self.client = self.app.test_client()  # Create a test client for the app

        # Create and add a user to the database
        self.hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        self.user = User(username='testuser', email='testuser@example.com', password=self.hashed_password)
        db.session.add(self.user)
        db.session.commit()  # Commit the changes

    def tearDown(self):
        db.session.remove()  
        db.drop_all()  
        self.app_context.pop()  

    def login(self):
        with self.app.test_request_context():
            return self.client.post(url_for('main.login'), data=dict(
                email='testuser@example.com',
                password='password'
            ), follow_redirects=True)  # Submit login data and follow redirects

    def test_search_function(self):
        with self.app.test_request_context():
            self.login()  # Ensure the user is logged in
            post = Post(title='Test Search Post', content='Searchable content', author=self.user)
            db.session.add(post)
            db.session.commit()  # Commit the post to the database

            response = self.client.post(url_for('main.search'), data=dict(
                searched='Searchable'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200
            self.assertIn(b'Searchable content', response.data)  # Assert that the response data contains 'Searchable content'

if __name__ == '__main__':
    unittest.main()  # Run the unit tests if this script is executed directly

