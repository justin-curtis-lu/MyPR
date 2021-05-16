import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dn32918hdnewqQDQd2qdeqx'

    # Database Config (SQLite for now -> Migrate to Server Db for deployment )
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['juclu@ucdavis.edu']

    POSTS_PER_PAGE = 5
    # LANGUAGES = ['en', 'es']
    # MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # TEMP DO NOT COMMIT AND SWITCH TO ENVIORNMENT VARIABLES FOR DEPLOYMENT
    # S3_BUCKET = 'mypr-images'
    # S3_KEY = ''
    # S3_SECRET = ''
    # S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
