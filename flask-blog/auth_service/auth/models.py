# -*- coding: utf-8 -*-

"""
Authentication-related models module.
"""

from typing import Tuple

from flask import current_app
from marshmallow import EXCLUDE, fields, validate

from . import db, ma


class User(db.Model):
    """
    User table for authentication.
    """
    __tablename__ = 'users'

    USERNAME_MAX_LEN = 120
    PASSWORD_MIN_LEN = 8
    PASSWORD_MAX_LEN = 60

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(USERNAME_MAX_LEN), nullable=False, unique=True, index=True
    )  # Since we'll frequently query usernames, we create an index on it.
    password = db.Column(db.String(PASSWORD_MAX_LEN), nullable=False)


class UserSchema(ma.Schema):
    """
    User schema.
    """

    id = fields.Integer(dump_only=True)
    username = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=User.USERNAME_MAX_LEN)
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(
            min=User.PASSWORD_MIN_LEN, max=User.PASSWORD_MAX_LEN
        ),
        load_only=True
    )

    class Meta:
        unknown = EXCLUDE


user_schema = UserSchema()