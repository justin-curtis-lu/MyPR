from app import db
from datetime import datetime
# Import werkzeug hashing for password security
from werkzeug.security import generate_password_hash, check_password_hash

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # Password hashes for application security
    password_hash = db.Column(db.String(128))
    # Connection from user model to post model
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # User set password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # User check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)