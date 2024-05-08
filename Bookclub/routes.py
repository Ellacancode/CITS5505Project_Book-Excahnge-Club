import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from Bookclub import app, db, bcrypt
from Bookclub.forms import (
    RegistrationForm, LoginForm, UpdateAccountForm, PostForm, SearchForm,
    CommentForm, EmptyForm, FollowForm, UnfollowForm
)
from Bookclub.models import User, Post, Book, Comment, Like
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime
from zoneinfo import ZoneInfo

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).all()
    follow_form = FollowForm()
    unfollow_form = UnfollowForm()
    form = EmptyForm()
    return render_template(
        'user.html',
        title='View User',
        user=user,
        posts=posts,
        follow_form=follow_form,
        unfollow_form=unfollow_form,
        form=form
    )

@app.route("/")
def home():
    return render_template('home.html', title='Home')

@app.route("/forum")
def forum():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('forum.html', posts=posts)

@app.route("/search_books", methods=['GET', 'POST'])
def search_books():
    results = []
    if request.method == 'POST':
        query = request.form.get('query')
        search_by = request.form.get('search_by')
        if search_by == 'book_title':
            results = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
        elif search_by == 'genre':
            results = Book.query.filter(Book.genre.ilike(f'%{query}%')).all()
        
        return render_template('book_result.html', results=results)
    return render_template('search_books.html')

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

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

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

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(ZoneInfo("Australia/Perth"))
        db.session.commit()

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
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        if form.picture.data:
            picture_file = upload_images(form.picture.data, 'static/post_images')
            post.image_file = picture_file
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('forum'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(to_post_id=post_id).all()

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(to_post_id=post_id, content=form.content.data, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been created!', 'success')
        return redirect(url_for('post', post_id=post_id))

    return render_template(
        'post.html',
        post=post,
        form=form,
        legend='New comment',
        comments=comments
    )

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
        if form.picture.data:
            picture_file = upload_images(form.picture.data, 'static/post_images')
            post.image_file = picture_file
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

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

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first_or_404()
        if user == current_user:
            flash('You cannot follow yourself!', 'danger')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are now following {username}!', 'success')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('forum'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first_or_404()
        if user == current_user:
            flash('You cannot unfollow yourself!', 'danger')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are no longer following {username}.', 'success')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('forum'))

@app.context_processor
def layout():
    form = SearchForm()
    return dict(form=form)

@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        post_searched = form.searched.data
        posts = posts.filter(Post.content.like(f'%{post_searched}%'))
        posts = posts.order_by(Post.title).all()
        return render_template(
            "search.html",
            form=form,
            searched=post_searched,
            posts=posts
        )
# Like route
@app.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        flash('You unliked the post!', 'info')
    else:
        new_like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        flash('You liked the post!', 'success')
    return redirect(url_for('post', post_id=post_id))


