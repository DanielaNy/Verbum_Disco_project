from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from VDP import config_file

app = Flask(__name__)
app.config.update(
    DEBUG=config_file.DEBUG,
    SECRET_KEY=config_file.SECRET_KEY,
    SQLALCHEMY_DATABASE_URI=config_file.SQLALCHEMY_DATABASE_URI,
    APP_ROOT=config_file.APP_ROOT,
    SQLALCHEMY_TRACK_MODIFICATIONS=config_file.SQLALCHEMY_TRACK_MODIFICATIONS)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
logger = logging.getLogger()

from VDP import routes
