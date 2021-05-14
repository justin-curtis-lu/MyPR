from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# App instance
app = Flask(__name__)

# FLASK EXTENSIONS

# Read in config values
app.config.from_object(Config)
# Read in Db
db = SQLAlchemy(app)
# Migration Engine
migrate = Migrate(app, db)
# Login handling
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

