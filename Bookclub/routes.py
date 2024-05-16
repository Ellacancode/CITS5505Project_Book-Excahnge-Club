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

# Home page route: Displays the home page
@app.route("/", methods=['GET'])
def home():
    return render_template('home.html', title='Home')

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


# Forum page route: Displays all posts on the forum page
@app.route("/forum")
def forum():
    # Add Pagination
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('forum.html', posts=posts)

# Search books route: Allows searching books by title, genre, author, status, or ISBN
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
        elif search_by == 'author':
            results = Book.query.filter(Book.author.ilike(f'%{query}%')).all()
        elif search_by == 'status':
            results = Book.query.filter(Book.status.ilike(f'%{query}%')).all()
        elif search_by == 'isbn':
            results = Book.query.filter(Book.isbn.ilike(f'%{query}%')).all()
        
        return render_template('book_result.html', results=results)
    return render_template('search_books.html')
     
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


def upload_images(form_picture, storage_path, output_size=(125, 125)):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(app.root_path, storage_path, picture_fn)

    i = Image.open(form_picture)
    i.thumbnail(output_size)  # Resize the image using the provided output_size

    if i.mode != 'RGB':
        i = i.convert('RGB')  # Convert image to RGB mode to ensure compatibility

    i.save(picture_path)
    return picture_fn

# Update last_seen before each request for authenticated users
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(ZoneInfo("Australia/Perth"))
        print(f"Updating last_seen to Perth time: {current_user.last_seen}")
        db.session.commit()

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
            picture_file = upload_images(form.picture.data, 'static/post_images',output_size=(500, 500))
            post.image_file = picture_file  # Ensure your Post model has an image_file field
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('forum'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

#comments     

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    allComments = Comment.query.filter_by(to_post_id=post_id).all()
    for i, comment_item in enumerate(allComments):
        class Comment_return:
            def __init__(self, content, to_post_id, author, image_file, date_posted):
                self.content = content
                self.to_post_id = to_post_id
                self.author = author  # author is now a User object
                self.image_file = image_file
                self.date_posted = date_posted

        user = User.query.filter_by(id=comment_item.user_id).first()
        allComments[i] = Comment_return(
            comment_item.content,
            comment_item.to_post_id,
            user,  # Pass the User object instead of just the username
            comment_item.image_file,
            comment_item.date_posted
        )

    form = CommentForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = upload_images(form.picture.data, 'static/comment_pics',output_size=(500,500))
        else:
            picture_file = 'default.jpg'

        comment = Comment(
            to_post_id=post_id,
            content=form.content.data,
            user_id=current_user.id,
            image_file=picture_file
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been created!', 'success')
        return redirect(url_for('post', post_id=post_id))

    return render_template('post.html', postTitle=post.title, post=post, form=form, legend='New comment', comments=allComments)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and current_user.email != 'admin@admin.com':
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = upload_images(form.picture.data, 'static/post_images')
            post.image_file = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    image_file = url_for('static', filename='profile_pics/' + post.image_file)
    return render_template('update_post.html', title='Update Post', form=form, legend='Update Post', image_file=image_file)

# Route to delete an existing post, requires login and user must be the author
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and current_user.email != 'admin@admin.com':
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('forum'))


#follow  route
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

#pass stuff to NavBar 
@app.context_processor
def layout():
    form = SearchForm()
    return dict(form=form)


# Create search function 
@app.route('/search', methods=["GET", "POST"])
def search():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        search_term = form.searched.data
        # Perform filtering using OR to search across multiple fields
        posts = posts.filter(
            (Post.title.ilike(f'%{search_term}%')) |
            (Post.date_posted.ilike(f'%{search_term}%')) |
            (Post.content.ilike(f'%{search_term}%')) |
            (Post.user_id == int(search_term) if search_term.isdigit() else False)
        ).order_by(Post.date_posted.desc()).all()

        return render_template("search.html",
                               form=form,
                               searched=search_term,
                               posts=posts)
    return render_template("search.html",
                           form=form,
                           searched='',
                           posts=[])

# bookshelf
@app.route("/shelf", methods=['GET', 'POST'])
@login_required
def shelf(): 
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        book = Book.query.get(book_id)
        if book:
            book.status = 'borrowed' if book.status == 'available' else 'available'
            db.session.commit()

    books = Book.query.order_by(Book.id.asc()).all()
    return render_template('shelf.html', title='BookShelf', books=books)