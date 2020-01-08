from flask import Flask, g
from flask_httpauth import HTTPBasicAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from .config import Config

db = SQLAlchemy()
ma = Marshmallow()
auth = HTTPBasicAuth()

from .utils import RATELIMIT_DEFAULT


def my_key_func() -> str:
    """
    Self-defined key function for rate limiting.
    :return: str
    """
    if 'username' in g:
        return g.username
    return get_remote_address()


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
    # Since we'll place this web service behind a proxy server (Nginx), in order
    # for rate-limiting to get the correct remote address from
    # "X-Forwarded-For" header, we need to do some extra setup here.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    limiter.init_app(app)

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

    # Implementation with extension:
    from .api import api_bp
    app.register_blueprint(api_bp)

    db.create_all(app=app)

    return app
