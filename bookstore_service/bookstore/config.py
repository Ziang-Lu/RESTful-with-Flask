# -*- coding: utf-8 -*-

"""
Flask application configurations module.
"""


class Config:
    """
    Flask application configuration class.
    """

    # Generate the secret key using secrets.token_hex(16)
    SECRET_KEY = '8bfbeeb3da58dddc3c2b8d15cf2a1904'

    # Configure the SQLAlchemy-related options
    postgres_user = 'postgres'
    postgres_password = 'password'
    postgres_hostname = 'db'
    postgres_db = 'bookstore'
    SQLALCHEMY_DATABASE_URI = f'postgres://{postgres_user}:{postgres_password}@{postgres_hostname}/{postgres_db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configure the Flask-Limiter related options
    redis_hostname = 'rate-limiting'
    redis_port = 6379
    RATELIMIT_STORAGE_URL = f'redis://{redis_hostname}:{redis_port}'
    RATELIMIT_KEY_PREFIX = 'rl'
    RATELIMIT_STRATEGY = 'fixed-window'  # To do more accurate rate limiting more, change this to "moving-window"
