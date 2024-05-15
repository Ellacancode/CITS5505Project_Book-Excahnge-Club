import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

# Create a Flask instance
app = Flask(__name__)

# Set the secret key for session management
app.config['SECRET_KEY'] = os.urandom(24)

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

#Debug
app.debug = True

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Flask-Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize Flask-Login for managing user sessions
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Specifies the login view function
login_manager.login_message_category = 'info' # Set the category for the flash message for non-logged-in users

# Setup Flask-Admin
admin = Admin(app, template_mode='bootstrap3')

# Import the User model here, before using it in ModelView
from .models import User
from .models import Post
from .models import Comment
from .models import Book
from .models import Like

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session)) 
admin.add_view(ModelView(Comment, db.session)) 
admin.add_view(ModelView(Book, db.session)) 
admin.add_view(ModelView(Like, db.session)) 

# Initialize Flask-Migrate for handling database migrations
migrate = Migrate(app, db)

# Import the routes
from Bookclub import routes
