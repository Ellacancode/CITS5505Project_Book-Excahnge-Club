# User model and database setup for Flask applications
from datetime import datetime
from Bookclub import db, login_manager
from flask_login import UserMixin

# Book model to represent books in the database
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(120), nullable=True)
    author = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    isbn = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(255))

# Function to load a user given their user ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model with fields and methods necessary for authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

#Post model to represent blog posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
