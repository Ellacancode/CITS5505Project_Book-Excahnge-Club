#verify the search books page is accessible and contains the expected content
import unittest
from flask import url_for
from flask_testing import TestCase
from Bookclub import create_app, db

class SearchBooksPageTestCase(TestCase):

    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()


    def test_search_books_page(self): # Define a test method for the search books page
        response = self.client.get(url_for('main.search_books'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search for books', response.data)# Assert that the response data contains 'Search for books'

if __name__ == '__main__':
    unittest.main()
