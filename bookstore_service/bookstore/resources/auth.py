# -*- coding: utf-8 -*-

"""
Authentication-related RESTful API module.
"""

import requests
from flask import g, request
from flask_limiter.util import get_remote_address
from flask_restful import Resource

from .. import auth, limiter
from ..utils import RATELIMIT_NORMAL, RATELIMIT_SLOW


class UserItem(Resource):
    """
    Resource for a single user.
    """
    decorators = [
        limiter.limit(
            RATELIMIT_NORMAL, key_func=get_remote_address, per_method=True
        )
    ]

    def post(self):
        """
        Adds a new user.
        :return:
        """
        r = requests.post(
            'http://auth_service:8000/users', json=request.get_json()
        )
        return r.json(), r.status_code


class Token(Resource):
    """
    Resource for token.
    """
    decorators = [
        auth.login_required,
        limiter.limit(RATELIMIT_SLOW, per_method=True)
    ]

    def get(self):
        """
        Gets a token for the current logged-in user.
        :return:
        """
        # After logging-in, we can access the username with "g.username"
        r = requests.get(
            'http://auth_service:8000/token', json={'username': g.username}
        )
        return r.json(), r.status_code
