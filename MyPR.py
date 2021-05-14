from app import app, db
from app.models import User, Post

# Flask shell for debugging in application context
# Work with related imports

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}