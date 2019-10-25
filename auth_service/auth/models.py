from typing import Tuple

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import db


class User(db.Model):
    """
    User table for authentication.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(120), nullable=False, unique=True, index=True
    )  # Since we'll frequently query usernames, we create an index on it.
    password = db.Column(db.String(60), nullable=False)

    def generate_token(self, expiration: int=600) -> Tuple[str, int]:
        """
        Generates a token with the given expiration time.
        :param expiration: int
        :return: tuple
        """
        serializer = Serializer(
            secret_key=current_app['SECRET_KEY'], expires_in=expiration
        )
        return serializer.dumps({'id': self.id}), expiration

    def __repr__(self):
        return f"User('{self.username}')"
