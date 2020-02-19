import os

# configuration of Flask app
configuration = 'dev'        # 'dev' or 'prod'


def configure_app(configuration='prod'):
    """configures flask app; default for production 'prod',
    if for development, set configuration to 'dev' above"""
    DEBUG = True
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if configuration == 'prod':
        DEBUG = False
        SECRET_KEY = os.urandom(16)

    return DEBUG, SECRET_KEY, SQLALCHEMY_DATABASE_URI, APP_ROOT, SQLALCHEMY_TRACK_MODIFICATIONS


DEBUG, SECRET_KEY, SQLALCHEMY_DATABASE_URI, APP_ROOT, SQLALCHEMY_TRACK_MODIFICATIONS = configure_app(
    configuration)


# configuration of game
db_name = "db.sqlite3"
file_txt = "user" + "_file.txt"
user_destination = os.path.join(APP_ROOT, 'user/')
file_in_user_destination = "/".join([user_destination, file_txt])
no_of_selected = 5
