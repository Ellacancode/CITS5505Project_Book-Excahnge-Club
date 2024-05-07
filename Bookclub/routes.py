import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from Bookclub import app, db, bcrypt # Main application, database, and encryption module imports
from Bookclub.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm # Import forms for user registration, login, and post creation
from Bookclub.models import User, Post, Book, Comment
from flask_login import login_user, current_user, logout_user, login_required  # Import functions for user session management
from werkzeug.utils import secure_filename


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

# Helper function to handle image file uploads within forms
def upload_images(form_picture, storage_path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, storage_path, picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# Profile update route, requires login to access
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = upload_images(form.picture.data, 'static/profile_pics')
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        current_user.last_seen = datetime.now(ZoneInfo("Australia/Perth"))
        print(f"Updating profile: {current_user.last_seen}")
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Profile',
                           image_file=image_file, form=form)


# Route to create a new post, requires login to access
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
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

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    allComments = Comment.query.filter_by(to_post_id=post_id).all()
    

    for i, comment_item in enumerate(allComments):
        class Comment_return:
            def __init__(self, content, to_post_id, author):
                self.content = content
                self.to_post_id = to_post_id
                self.author = author
        allComments[i] = Comment_return( comment_item.content, comment_item.to_post_id, User.query.filter_by(id=comment_item.user_id).first().username)
    form = CommentForm()
    

    if form.validate_on_submit():
        comment = Comment(to_post_id=post_id, content=form.content.data, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('post.html', postTitle=post.title, post=post,
                           form=form, legend='New comment', comments=allComments)

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

# Route to delete an existing post, requires login and user must be the author
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


#pass stuff to NavBar 
@app.context_processor
def layout():
    form = SearchForm()
    return dict(form=form)


