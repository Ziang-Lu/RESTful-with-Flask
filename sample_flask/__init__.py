from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_class=Config) -> Flask:
    """
    Application factory.
    :param config_class:
    :return: Flask
    """
    app = Flask(__name__)
    # Load configuration values from the configuration class
    app.config.from_object(config_class)

    # Initialize the SQLAlchemy object with the newly created application
    db.init_app(app)
    # Initialize the Marshmallow object with the newly created application
    ma.init_app(app)
    # Order matters: Initialize SQLAlchemy before Marshmallow

    # Naive implementation:
    # from sample_flask.naive_api.author import author_bp
    # app.register_blueprint(author_bp)
    # from sample_flask.naive_api.book import book_bp
    # app.register_blueprint(book_bp)

    # Implementation with extension:
    from sample_flask.api import api_bp
    app.register_blueprint(api_bp)

    # Initialize the database
    with app.app_context():
        db.create_all()

    return app
