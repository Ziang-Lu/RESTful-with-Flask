from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from flask_limiter import Limiter
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from werkzeug import middleware

from .config import Config

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
auth = HTTPBasicAuth()

from .utils import RATELIMIT_DEFAULT

URL_PREFIX_V1 = '/v1'  # For API versioning


def my_key_func() -> str:
    """
    Self-defined key function for rate limiting.
    Since most of the time, rate limiting is done after authentication, we can
    use "g.user.username" as the key.
    :return: str
    """
    return g.user.username


limiter = Limiter(default_limits=[RATELIMIT_DEFAULT], key_func=my_key_func)


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
    bcrypt.init_app(app)
    # Since we'll place this web service behind a proxy server (Nginx), in order
    # for rate-liminting to get the correct remote address from
    # "X-Forwarded-For" header, we need to do some extra setup here.
    app.wsgi_app = middleware.proxy_fix.ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1
    )
    limiter.init_app(app)

    # In order to make sure that all the routes are prefixed with
    # APPLICATION_ROOT, we need to do some extra setup here.
    app.wsgi_app = middleware.dispatcher.DispatcherMiddleware(
        app=Flask('dummy_app'),
        mounts={app.config['APPLICATION_ROOT']: app.wsgi_app}
    )

    # Authentication-related stuff
    # from .utils import verify_password_or_token
    # from .naive_api.auth import auth_bp
    # app.register_blueprint(auth_bp)

    # Naive implementation:
    # from .naive_api.author import author_bp
    # app.register_blueprint(author_bp)
    # from .naive_api.book import book_bp
    # app.register_blueprint(book_bp)

    # Implementation with extension:
    from .api import api_bp
    app.register_blueprint(api_bp)

    # Initialize the database
    with app.app_context():
        db.create_all()

    return app
