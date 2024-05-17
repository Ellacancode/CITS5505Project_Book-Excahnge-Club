#verify  the forum page is accessible and contains the expected content. 
import unittest
from flask import url_for
from flask_testing import TestCase
from Bookclub import create_app, db

class ForumPageTestCase(TestCase):

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

    def test_forum_page(self): # Define a test method for the forum page
        response = self.client.get(url_for('main.forum'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Forum', response.data)# Assert that the response data contains 'Forum'

if __name__ == '__main__':
    unittest.main()
