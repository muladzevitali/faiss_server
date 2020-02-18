"""Flask initialization"""
__author__ = "Vitali Muladze"

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models.log import Logger

# Database variable for connection
db = SQLAlchemy()


def create_app(config) -> Flask:
    # Create a flask application
    application = Flask(__name__)
    application.config.from_object(config)
    # Initialize the database connection within an application
    db.init_app(application)
    application.logger = Logger().get_logger()

    return application
