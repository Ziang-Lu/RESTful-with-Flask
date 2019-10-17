# -*- coding: utf-8 -*-

"""
Utility functions.
"""

from typing import Optional

from flask import current_app, g
from itsdangerous import (
    BadSignature, SignatureExpired,
    TimedJSONWebSignatureSerializer as Serializer
)

from . import auth, bcrypt
from .models import User


@auth.verify_password
def verify_password_or_token(username_or_token: str, password: str) -> bool:
    """
    Verifies the given username and password combination, or the given token as
    the username parameter.
    This function is automatically called by auth.login_required
    :param username_or_token: str
    :param password: str
    :return: bool
    """
    # Verify as if username_or_token is a token
    user = _verify_token(username_or_token)
    if user:
        g.user = user
        return True

    # Verify the username and password combination
    user = User.query.filter_by(username=username_or_token).first()
    if user and bcrypt.check_password_hash(user.password, password):
        g.user = user
        return True
    return False


def _verify_token(token: str) -> Optional[User]:
    """
    Helper function to verify the given token.
    :param token: str
    :return: User or None
    """
    serializer = Serializer(secret_key=current_app['SECRET_KEY'])
    try:
        data = serializer.loads(token)
    except SignatureExpired:  # Valid token, but expired
        return None
    except BadSignature:  # Invalid token
        return None
    return User.query.get(data['id'])


RATELIMIT_DEFAULT = '1 per second'
RATELIMIT_NORMAL = '20 per minute'
RATELIMIT_SLOW = '1 per minute'
