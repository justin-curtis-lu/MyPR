import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dn32918hdnewqQDQd2qdeqx'

    # Database Config (SQLite for now -> Migrate to Server Db for deployment )
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                           'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = (os.environ.get("DATABASE_URL") + "?sslmode=require").replace("postgres://", "postgresql://", 1) or \
                              'sqlite:///' + os.path.join(basedir,'app.db')
    print(SQLALCHEMY_DATABASE_URI)
    # SQLALCHEMY_DATABASE_URI = (os.environ.get("DATABASE_URL") + "?sslmode=require") or \
    #                               "sqlite: // / " + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['juclu@ucdavis.edu']
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    POSTS_PER_PAGE = 5
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')