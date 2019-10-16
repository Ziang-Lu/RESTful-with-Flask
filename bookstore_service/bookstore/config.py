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
    # Configure the SQLAlchemy database connection URI
    POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = 'password'
    POSTGRES_HOSTNAME = 'db'
    POSTGRES_DB = 'bookstore'
    SQLALCHEMY_DATABASE_URI = f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}/{POSTGRES_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
