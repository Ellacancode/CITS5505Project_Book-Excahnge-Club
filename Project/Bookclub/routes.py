import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from Bookclub import app, db, bcrypt # Main application, database, and encryption module imports
from Bookclub.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, SearchForm 
from Bookclub.models import User, Post, Book
from flask_login import login_user, current_user, logout_user, login_required  # Import functions for user session management

# Home page route: Displays the home page
@app.route("/")
def home():
    return render_template('home.html', title='Home')

     
#User registration route handling GET and POST requests, implements registration functionality
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Login route for handling user logins with form validation and session management
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Logout route to handle user session termination
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

