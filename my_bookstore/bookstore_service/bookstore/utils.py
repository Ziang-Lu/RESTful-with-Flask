# -*- coding: utf-8 -*-

"""
Utility functions.
"""

import functools
import requests
from typing import Callable

from flask import g, request, url_for
from flask_marshmallow import Schema

from . import auth


# If we want to use "auth.login_required" decorator on routes, we need to
# provide an implementation to "auth.verify_password"
@auth.verify_password
def verify_password_or_access_token(username_or_token: str,
                                    password: str) -> bool:
    """
    Verifies the given username and password combination, or the given access
    token as the username parameter.
    This function is automatically called by auth.login_required
    :param username_or_token: str
    :param password: str
    :return: bool
    """
    r = requests.get(
        'http://auth_service:8000/user-auth',
        json={
            'username_or_token': username_or_token,
            'password': password
        }
    )
    if r.status_code == 401:
        return False
    # Save the found username for the current request processing
    g.username = r.json()['data']
    return True


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
                'total': p.total
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
