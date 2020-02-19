from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from VDP.config_file import *

app = Flask(__name__)
app.config.update(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
    APP_ROOT=APP_ROOT,
    SQLALCHEMY_TRACK_MODIFICATIONS=SQLALCHEMY_TRACK_MODIFICATIONS)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
logger = logging.getLogger()

from VDP import routes
