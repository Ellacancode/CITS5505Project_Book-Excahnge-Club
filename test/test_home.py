import unittest  # Import the unittest module for creating unit tests
from flask_testing import TestCase  # Import TestCase from flask_testing for testing Flask applications
from Bookclub import create_app, db  # Import create_app and db from the Bookclub module

class HomePageTestCase(TestCase):  # Define a test case class that inherits from TestCase

    def create_app(self):  # Method to create the Flask application
        app = create_app('testing')  # Create the Flask app with the 'testing' configuration
        return app  # Return the created app

    def setUp(self):  # Method that runs before each test
        self.client = self.app.test_client()  # Create a test client for the app
        with self.app.app_context():  # Push the application context
            db.create_all()  # Create all database tables

    def tearDown(self):  # Method that runs after each test
        with self.app.app_context():  # Push the application context
            db.session.remove()  # Remove the database session
    

    def test_home_page(self):  # Define a test method for the home page
        response = self.client.get('/')  # Send a GET request to the home page
        self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200
        self.assertIn('Building community at UWA through books', response.data.decode())  # Assert that the response data contains the expected text

if __name__ == '__main__':  
    unittest.main()  # Run the unit tests

