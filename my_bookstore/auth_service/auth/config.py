# -*- coding: utf-8 -*-

"""
Flask application configurations module.
"""

import os


class Config:
    """
    Flask application configuration class.
    """

    # Generate the secret key using secrets.token_hex(16)
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']

    # Configure the SQLAlchemy-related options
    postgres_user = os.environ['POSTGRES_USER']
    postgres_password = os.environ['POSTGRES_PASSWORD']
    postgres_hostname = 'db'
    postgres_db = 'bookstore'
    SQLALCHEMY_DATABASE_URI = f'postgres://{postgres_user}:{postgres_password}@{postgres_hostname}/{postgres_db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
