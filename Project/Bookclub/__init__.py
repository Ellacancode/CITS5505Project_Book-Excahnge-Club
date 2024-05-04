from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
from flask_migrate import Migrate

# Create a Flask instance
app = Flask(__name__)

# Set the secret key for session management
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Flask-Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize Flask-Login for managing user sessions
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Specifies the login view function
login_manager.login_message_category = 'info' # Set the category for the flash message for non-logged-in users

# Initialize Flask-Migrate for handling database migrations
migrate = Migrate(app, db)

# Import the routes
from Bookclub import routes
