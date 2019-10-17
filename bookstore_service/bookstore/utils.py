# -*- coding: utf-8 -*-

"""
Utility functions.
"""

import functools
from typing import Callable, Optional

from flask import current_app, g, request, url_for
from flask_marshmallow import Schema
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


def paginate(collection_schema: Schema, max_per_page: int=10) -> Callable:
    """
    Pagination decorator, with the collections serialized using the given
    collection schema.
    :param collection_schema: Schema
    :param max_per_page: int
    :return: Callable
    """
    def decorator(f: Callable) -> Callable:

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            page = request.args.get('page', type=int, default=1)
            per_page = min(
                request.args.get('per_page', type=int, default=10), max_per_page
            )

            query = f(*args, **kwargs)
            p = query.paginate(page=page, per_page=per_page)
            # "p" is a Pagination object.

            # Populate the pagination metadata
            pagination_meta = {
                'page': page,
                'per_page': per_page,
                'pages': p.pages,
                'total': p.total,
            }
            if p.has_prev:
                pagination_meta['prev'] = url_for(
                    request.endpoint, page=p.prev_num, per_page=per_page,
                    _external=True
                )
            else:
                pagination_meta['prev'] = None
            if p.has_next:
                pagination_meta['next'] = url_for(
                    request.endpoint, page=p.next_num, per_page=per_page,
                    _external=True
                )
            else:
                pagination_meta['next'] = None
            pagination_meta['first'] = url_for(
                request.endpoint, page=1, per_page=per_page, _external=True
            )
            pagination_meta['last'] = url_for(
                request.endpoint, page=p.pages, per_page=per_page,
                _external=True
            )

            return {
                'status': 'success',
                'data': collection_schema.dump(p.items),
                'pagination_meta': pagination_meta
            }, 200
        return wrapper

    return decorator


RATELIMIT_DEFAULT = '1 per second'
RATELIMIT_NORMAL = '20 per minute'
RATELIMIT_SLOW = '1 per minute'
