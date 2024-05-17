import unittest  # Import the unittest module for creating unit tests
from flask import url_for  # Import url_for to build URLs for the application
from Bookclub import create_app, db, bcrypt  # Import necessary components from the Bookclub module
from Bookclub.models import User, Post  # Import models to be tested

# Purpose: To verify post creation, viewing, updating, and deletion
class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')  
        self.app_context = self.app.app_context()  
        self.app_context.push()  
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

    def login(self):
        with self.app.test_request_context():
            return self.client.post(url_for('main.login'), data=dict(
                email='testuser@example.com',
                password='password'
            ), follow_redirects=True)  # Submit login data and follow redirects

    def test_create_post(self):
        with self.app.test_request_context():
            # Log in to access the new post page
            self.login()
            response = self.client.get(url_for('main.new_post'))
            self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200
            self.assertIn(b'New Post', response.data)  # Assert that the response data contains 'New Post'

            # Create a new post
            response = self.client.post(url_for('main.new_post'), data=dict(
                title='Test Post',
                content='This is a test post content.'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200
            self.assertIn(b'Your post has been created!', response.data)  # Assert that the response data contains success message

    def test_post_page(self):
        with self.app.test_request_context():
            # Log in to create a post
            self.login()
            post = Post(title='Test Post', content='This is a test post content.', author=self.user)
            db.session.add(post)
            db.session.commit()  # Commit the post to the database

            # View the post page
            response = self.client.get(url_for('main.post', post_id=post.id))
            self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200
            self.assertIn(b'Test Post', response.data)  # Assert that the response data contains the post title

    def test_update_post(self):
        with self.app.test_request_context():
            # Log in to create a post
            self.login()
            post = Post(title='Test Post', content='This is a test post content.', author=self.user)
            db.session.add(post)
            db.session.commit()  # Commit the post to the database

            # Access the update post page
            response = self.client.get(url_for('main.update_post', post_id=post.id))
            self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200
            self.assertIn(b'Update Post', response.data)  # Assert that the response data contains 'Update Post'

            # Update the post
            response = self.client.post(url_for('main.update_post', post_id=post.id), data=dict(
                title='Updated Post',
                content='This is updated content.'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200
            self.assertIn(b'Your post has been updated!', response.data)  # Assert that the response data contains success message

    def test_delete_post(self):
        with self.app.test_request_context():
            # Log in to create a post
            self.login()
            post = Post(title='Test Post', content='This is a test post content.', author=self.user)
            db.session.add(post)
            db.session.commit()  # Commit the post to the database

            # Delete the post
            response = self.client.post(url_for('main.delete_post', post_id=post.id), follow_redirects=True)
            self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200
            self.assertIn(b'Your post has been deleted!', response.data)  # Assert that the response data contains success message

if __name__ == '__main__':
    unittest.main()  # Run the unit tests if this script is executed directly

