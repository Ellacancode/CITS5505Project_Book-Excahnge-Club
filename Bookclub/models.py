from datetime import datetime
from zoneinfo import ZoneInfo
from Bookclub import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship

# Follow table to manage followers
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id', name='fk_followers_follower_id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id', name='fk_followers_followed_id'))
)

# Load user with flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    about_me = db.Column(db.String(250), nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)

    following_relationship = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers_relationship'
    )

    followers_relationship = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following_relationship'
    )

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.about_me}', '{self.last_seen}')"

    def followers_count(self):
        return len(self.followers_relationship)

    def following_count(self):
        return len(self.following_relationship)

    def is_following(self, user):
        return user in self.following_relationship

    def is_followed_by(self, user):
        return user in self.followers_relationship

    def follow(self, user):
        if not self.is_following(user):
            self.following_relationship.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following_relationship.remove(user)

    def like_post(self, post):
        if not self.has_liked_post(post):
            post.likes.append(self)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            post.likes.remove(self)

    def has_liked_post(self, post):
        return Like.query.filter_by(user_id=self.id, post_id=post.id).first() is not None

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(50), nullable=True, default='default.jpg')
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name='fk_post_user', ondelete='CASCADE'),
        nullable=False
    )
    comments = db.relationship('Comment', backref='post', lazy=True, passive_deletes=True)
    likes = db.relationship('Like', backref='post', lazy=True, passive_deletes=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.image_file}')"

    def is_liked_by_user(self, user):
        if not user.is_authenticated:
            return False
        return Like.query.filter_by(user_id=user.id, post_id=self.id).first() is not None

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id', name='fk_comment_post', ondelete='CASCADE'),
        nullable=False
    )
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(50), nullable=True, default='default.jpg')
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name='fk_comment_user', ondelete='CASCADE'),
        nullable=False
    )

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}', '{self.image_file}')"

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id', name='fk_like_post', ondelete='CASCADE'),
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', name='fk_like_user', ondelete='CASCADE'),
        nullable=False
    )
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Like('User ID: {self.user_id}', 'Post ID: {self.post_id}', '{self.date_posted}')"

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(120), nullable=True)
    author = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    isbn = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(255), nullable=True)
