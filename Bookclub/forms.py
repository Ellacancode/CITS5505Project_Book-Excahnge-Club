# Import FlaskForm from flask_wtf to create form classes
from flask_wtf import FlaskForm

# Import FileField and FileAllowed for handling file uploads and validation
from flask_wtf.file import FileField, FileAllowed

# Import current_user from flask_login to access the current logged-in user
from flask_login import current_user

# Import various fields and validators from wtforms to build form fields and add validation
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp

# Import the User model from Bookclub.models to query the database for user validation
from Bookclub.models import User


# Form for registeration
class RegistrationForm(FlaskForm):
       # length between 2 and 15 characters
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=15)])  # Username length between 2 and 15
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters"),
        Regexp(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]',
            message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
        )
    ])
    # Confirm Password field with validation
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')

    # check if the username is already taken
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Sorry, the username is unavailable, please choose another one.')
    #check if the email is already registered
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Sorry, the email is unavailable, please choose a different one.')

# Form for user login
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Form for updating user account information
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    # image_file = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=250)])
    submit = SubmitField('Update')

    # Custom validator to check if the username is taken and it's not the current user's
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    # Custom validator to check if the email is taken and it's not the current user's
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

# Form for creating or editing a post
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    # image_file = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Post')

# Form for creating a comment
class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Upload Comment Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Post')

# Form for search functionality
class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit") 

# Empty form for CSRF protection
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

# Form for following users
class FollowForm(FlaskForm):
    submit = SubmitField('Follow', validators=[DataRequired()])

# Form for unfollowing users
class UnfollowForm(FlaskForm):
    submit = SubmitField('Unfollow', validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Reset Password")

