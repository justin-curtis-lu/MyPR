from flask import render_template
from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app.models import User
from flask import request
from werkzeug.urls import url_parse

# Landing Page
@app.route('/')
@app.route('/index')
# Block on non logged in users
@login_required
def index():
    user = {'username': 'Justin'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Bench PR!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'Squat PR!'
        }
    ]
    return render_template('index.html', title='Home',  posts=posts)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # get LoginForm
    form = LoginForm()
    # Form processing
    if form.validate_on_submit():
        # Query db for username
        user = User.query.filter_by(username=form.username.data).first()
        # Invalid user or password
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Valid user -> flash message and return index
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    # False -> Reload login page
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))