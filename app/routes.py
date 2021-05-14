from flask import render_template
from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for

# Landing Page
@app.route('/')
@app.route('/index')
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
    return render_template('index.html', title='Home', user=user, posts=posts)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # get LoginForm
    form = LoginForm()
    # Form processing
    if form.validate_on_submit():
        # True -> flash message and return index
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    # False -> Reload login page
    return render_template('login.html', title='Sign In', form=form)