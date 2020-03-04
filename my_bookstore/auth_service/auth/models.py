# -*- coding: utf-8 -*-

"""
Authentication-related models module.
"""

from typing import Tuple

from flask import current_app
from itsdangerous import (
    BadSignature, SignatureExpired,
    TimedJSONWebSignatureSerializer as Serializer
)
from marshmallow import EXCLUDE, fields, validate

from . import db, ma


class User(db.Model):
    """
    User table for authentication.
    """
    __tablename__ = 'users'

    USERNAME_MAX_LEN = 120
    EMAIL_MAX_LEN = 50
    PASSWORD_MIN_LEN = 8
    PASSWORD_MAX_LEN = 60

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(USERNAME_MAX_LEN), nullable=False, unique=True, index=True
    )  # Since we'll frequently query usernames, we create an index on it.
    email = db.Column(db.String(EMAIL_MAX_LEN), unique=True)
    password = db.Column(db.String(PASSWORD_MAX_LEN), nullable=False)

    @staticmethod
    def verify_token(token: str):
        """
        Static method to verify the given token.
        :param token: str
        :return: User or None
        """
        serializer = Serializer(secret_key=current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except SignatureExpired:  # Valid token, but expired
            return None
        except BadSignature:  # Invalid token
            return None
        found_user = User.query.get(data['id'])
        return found_user

    def gen_token(self, expires_in: int=600) -> Tuple[str, int]:
        """
        Generates a user token with the given expiration time.
        :param expires_in: int
        :return: tuple(str, int)
        """
        serializer = Serializer(
            secret_key=current_app.config['SECRET_KEY'], expires_in=expires_in
        )
        return serializer.dumps({'id': self.id}), expires_in


class UserSchema(ma.Schema):
    """
    User schema.
    """

    id = fields.Integer(dump_only=True)
    username = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=User.USERNAME_MAX_LEN)
    )
    email = fields.Email(
        validate=validate.Length(min=1, max=User.EMAIL_MAX_LEN)
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
