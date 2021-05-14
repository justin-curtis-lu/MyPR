from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# Read in config values
app.config.from_object(Config)
# Read in Db
db = SQLAlchemy(app)
# Migration Engine
migrate = Migrate(app, db)

from app import routes, models

