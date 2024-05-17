import unittest  # Import the unittest module for creating unit tests
from flask import url_for  # Import url_for to build URLs for the application
from Bookclub import create_app, db, bcrypt  # Import necessary components from the Bookclub module
from Bookclub.models import User, Post  # Import models to be tested

# Purpose: To verify follow/unfollow and like/unlike functionality
class FollowLikeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing') 
        self.app_context = self.app.app_context()  
        self.app_context.push()  
        db.create_all()  # Create all database tables
        self.client = self.app.test_client()  # Create a test client for the app

        # Create and add users to the database
        self.hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        self.user = User(username='testuser', email='testuser@example.com', password=self.hashed_password)
        self.admin = User(username='admin', email='admin@example.com', password=self.hashed_password)
        db.session.add(self.user)
        db.session.add(self.admin)
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

    def test_follow_unfollow_user(self):
        with self.app.test_request_context():
            self.login()
            follow_response = self.client.post(url_for('main.follow', username='admin'), follow_redirects=True)
            self.assertEqual(follow_response.status_code, 200)
            self.assertIn(b'You are now following admin!', follow_response.data)

            unfollow_response = self.client.post(url_for('main.unfollow', username='admin'), follow_redirects=True)
            self.assertEqual(unfollow_response.status_code, 200)
            self.assertIn(b'You are no longer following admin.', unfollow_response.data)

    def test_like_unlike_post(self):
        with self.app.test_request_context():
            self.login()
            post = Post(title='Test Post', content='This is a test post content.', author=self.user)
            db.session.add(post)
            db.session.commit()

            like_response = self.client.post(url_for('main.like_post', post_id=post.id), follow_redirects=True)
            self.assertEqual(like_response.status_code, 200)
            self.assertIn(b'You liked the post!', like_response.data)

            unlike_response = self.client.post(url_for('main.like_post', post_id=post.id), follow_redirects=True)
            self.assertEqual(unlike_response.status_code, 200)
            self.assertIn(b'You unliked the post!', unlike_response.data)

if __name__ == '__main__':
    unittest.main()  # Run the unit tests if this script is executed directly
