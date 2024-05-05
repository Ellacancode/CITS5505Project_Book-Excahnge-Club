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

# Forum page route: Displays all posts on the forum page
@app.route("/forum")
def forum():
    # Retrieve posts ordered by 'date_posted' descending
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('forum.html', posts=posts)

     
#User registration route handling GET and POST requests, implements registration functionality
@app.route("/register", methods=['GET', 'POST'])
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



# Route to create a new post, requires login to access
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        #upload the images when posting
        if form.picture.data:
            print(form.picture.data)
            picture_file = upload_images(form.picture.data, 'static/post_images')
            post.image_file = picture_file  # Ensure your Post model has an image_file field
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('forum'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

# Route to display a specific post by its ID
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# Route to update an existing post, requires login and user must be the author
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

# Route to delete a post, requires login and user must be the author
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('forum'))




