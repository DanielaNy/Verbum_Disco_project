import os


# configuration of the game
db_name = "db.sqlite3" # db in APP_ROOT
no_of_selected = 5
project_dir = os.path.dirname(os.path.dirname( __file__ ))
file_txt = "user" + "_file.txt"
user_destination = os.path.join(project_dir, 'user')
file_in_user_destination = "/".join([user_destination, file_txt])
sample_txt = "sample.txt"
sample_destination = os.path.join(project_dir, 'sample')
file_in_sample_destination = "/".join([sample_destination, sample_txt])
# levels = [0, 1, 2, 0, 0, 1, 0, 0, 0, 1]


# configuration of the Flask app
configuration = 'dev'        # 'dev' or 'prod'


def configure_app(configuration='prod'):
    """configures flask app; default for production 'prod',
    if for development, set configuration to 'dev' above"""
    DEBUG = True
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(project_dir, 'db.sqlite3')
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if configuration == 'prod':
        DEBUG = False
        SECRET_KEY = os.urandom(16)

    return DEBUG, SECRET_KEY, SQLALCHEMY_DATABASE_URI, APP_ROOT, SQLALCHEMY_TRACK_MODIFICATIONS


DEBUG, SECRET_KEY, SQLALCHEMY_DATABASE_URI, APP_ROOT, SQLALCHEMY_TRACK_MODIFICATIONS = configure_app(
    configuration)
