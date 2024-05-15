from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

# Add test class configuration
class TestConfig:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba244'  # Use a different secret key for testing
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # Test database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

# Create a Flask instance
app = Flask(__name__)

# Based on the environment, load the configuration
if os.getenv('APP_ENV') == 'testing':
    app.config.from_object(TestConfig)  # Directly pass the class object
else:
    # Development and production configuration
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///project.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Debug
app.debug = True

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Flask-Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize Flask-Login for managing user sessions
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specifies the login view function
login_manager.login_message_category = 'info'  # Set the category for the flash message for non-logged-in user

# Setup Flask-Admin
admin = Admin(app, template_mode='bootstrap3')

# Import the User model here, before using it in ModelView
from .models import User, Post, Comment, Book, Like

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(Like, db.session))

# Initialize Flask-Migrate for handling database migrations
migrate = Migrate(app, db)


#Register Blueprint
from Bookclub.routes  import main as main_blueprint
app.register_blueprint(main_blueprint)

# Import the routes

from Bookclub import routes

