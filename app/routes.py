from flask import render_template
from app import app

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