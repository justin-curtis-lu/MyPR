from flask import Flask
from config import Config

app = Flask(__name__)
# Read in config values
app.config.from_object(Config)

from app import routes