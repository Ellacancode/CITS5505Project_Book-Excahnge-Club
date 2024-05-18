import unittest
from datetime import datetime
from Bookclub import create_app, db, bcrypt
from Bookclub.models import User, Post, Comment, Like, Book

# Test case for User model
class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')  # Create the Flask application with the 'testing' configuration
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()  # Create a test client for the app
# Create and add two users to the database
        self.hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        self.user1 = User(username='user1', email='user1@example.com', password=self.hashed_password)
        self.user2 = User(username='user2', email='user2@example.com', password=self.hashed_password)
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User.query.filter_by(username='user1').first()  # Query the user by username
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'user1@example.com') # Check the user's email

# Test case for Post model
class PostModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
# Create and add a user to the database
        self.hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        self.user = User(username='user', email='user@example.com', password=self.hashed_password)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_post_creation(self):
        post = Post(title='Post 1', content='Post content', author=self.user)
        db.session.add(post)
        db.session.commit()

        post_from_db = Post.query.filter_by(title='Post 1').first()# Query the post by title
        self.assertIsNotNone(post_from_db)
        self.assertEqual(post_from_db.content, 'Post content') # Check the post content

# Test case for Comment model
class CommentModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        self.user = User(username='user', email='user@example.com', password=self.hashed_password)
        self.post = Post(title='Post 1', content='Post content', author=self.user)
        db.session.add(self.user)
        db.session.add(self.post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_comment_creation(self):
        comment = Comment(content='Comment content', user=self.user, post=self.post)
        db.session.add(comment)
        db.session.commit()

        comment_from_db = Comment.query.filter_by(content='Comment content').first() # Query the comment by content
        self.assertIsNotNone(comment_from_db)
        self.assertEqual(comment_from_db.content, 'Comment content') # Check the comment content

# Test case for Like model
class LikeModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
# Create and add a user and a post to the database
        self.hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        self.user = User(username='user', email='user@example.com', password=self.hashed_password)
        self.post = Post(title='Post 1', content='Post content', author=self.user)
        db.session.add(self.user)
        db.session.add(self.post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_like_creation(self):
        like = Like(user_id=self.user.id, post_id=self.post.id)
        db.session.add(like)
        db.session.commit()

        like_from_db = Like.query.filter_by(user_id=self.user.id, post_id=self.post.id).first() # Query the like by user_id and post_id
        self.assertIsNotNone(like_from_db)

# Test case for Book model
class BookModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_book_creation(self):
        # Create and add a book to the database
        book = Book(title='Book Title', genre='Fiction', author='Author Name', status='Available', isbn='1234567890', description='Book description')
        db.session.add(book)
        db.session.commit()

        book_from_db = Book.query.filter_by(title='Book Title').first() # Query the book by title
        self.assertIsNotNone(book_from_db)
        self.assertEqual(book_from_db.author, 'Author Name')  # Check the book author

if __name__ == '__main__':
    unittest.main()# Run the unit tests if this script is executed directly


