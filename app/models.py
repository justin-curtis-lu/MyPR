from app import db
from datetime import datetime
# Import werkzeug hashing for password security
from werkzeug.security import generate_password_hash, check_password_hash
# Mixin class for user implementations (authenticated, etc.)
from flask_login import UserMixin
from app import login
from hashlib import md5

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # Password hashes for application security
    password_hash = db.Column(db.String(128))
    # Connection from user model to post model
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # User set password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # User check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

# Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

# Flask User session
# Loading user
@login.user_loader
def load_user(id):
    return User.query.get(int(id))