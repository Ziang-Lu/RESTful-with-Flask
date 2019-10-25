from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
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
    bcrypt.init_app(app)

    # Implementation with extension:
    from .api import api_bp
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app
