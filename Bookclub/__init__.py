from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail

# Add test class configuration
class TestConfig:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba244'  # Use a different secret key for testing
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # Test database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

#reset password through email
mail = Mail()

# Set up configuration
def create_app(config_name=None):
    app = Flask(__name__)

    if config_name == 'testing':
        app.config.from_object(TestConfig)
    else:
        app.config['SECRET_KEY'] = os.urandom(24)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///project.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USERNAME'] = 'lucychenhello@gmail.com'
        app.config['MAIL_PASSWORD'] = 'ptlk akla vkgq qdah' #app password
        app.config['MAIL_DEFAULT_SENDER'] = 'lucychenhello@gmail.com' 

    # Debug
    app.debug = True

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Specifies the login view function
    login_manager.login_message_category = 'info'  # Set the category for the flash message for non-logged-in user
    migrate.init_app(app, db)
    mail.init_app(app)

    # Setup Flask-Admin
    admin = Admin(app, template_mode='bootstrap3')

    # Import the User model here, before using it in ModelView
    from .models import User, Post, Comment, Book, Like

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(ModelView(Book, db.session))
    admin.add_view(ModelView(Like, db.session))

    # Register Blueprint
    from Bookclub.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Import the routes
    from Bookclub import routes

    return app

