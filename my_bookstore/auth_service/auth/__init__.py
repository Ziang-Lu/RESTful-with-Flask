from flask import Flask
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()


def create_app(config=Config) -> Flask:
    """
    Application factory.
    :param config:
    :return: Flask
    """
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    ma.init_app(app)  # Order matters: Initialize SQLAlchemy before Marshmallow
    bcrypt.init_app(app)

    # Implementation with extension:
    from .api import api_bp
    app.register_blueprint(api_bp)

    # Create and initialize the database
    db.create_all(app=app)

    return app
