from flask import Flask, g
from flask_httpauth import HTTPBasicAuth
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from .config import Config

db = SQLAlchemy()
ma = Marshmallow()
auth = HTTPBasicAuth()


def create_app(config_class=Config) -> Flask:
    """
    Application factory.
    :param config_class:
    :return: Flask
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)  # Order matters: Initialize SQLAlchemy before Marshmallow

    # In order to make sure that all the routes are prefixed with
    # APPLICATION_ROOT, we need to do some extra setup here.
    app.wsgi_app = DispatcherMiddleware(
        app=Flask('dummy_app'),
        mounts={f"/{app.config['APPLICATION_ROOT']}": app.wsgi_app}
    )

    from .entrance import entrance_bp
    app.register_blueprint(entrance_bp)

    # Authentication-related stuff
    from .utils import verify_password_or_token

    from .api import api_bp
    app.register_blueprint(api_bp)

    # Create and initialize the database
    db.create_all(app=app)

    return app
