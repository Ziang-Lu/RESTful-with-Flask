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

    APPLICATION_ROOT = 'bookstore'  # Make sure that the routes are prefixed with "/bookstore"

    # Configure the SQLAlchemy-related options
    postgres_user = 'postgres'
    postgres_password = 'password'
    postgres_hostname = 'db'
    postgres_db = 'bookstore'
    SQLALCHEMY_DATABASE_URI = f'postgres://{postgres_user}:{postgres_password}@{postgres_hostname}/{postgres_db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
