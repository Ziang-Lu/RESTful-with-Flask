# -*- coding: utf-8 -*-

"""
Authentication-related RESTful API module.
"""

import requests
from flask import g, request
from flask_limiter.util import get_remote_address
from flask_restful import Resource
from marshmallow import ValidationError

from .. import auth, limiter
from ..models import user_schema
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
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as e:
            return {
                'message': e.messages
            }, 400

        r = requests.post('http://auth_service:8000/users', json=user_data)
        if r.status_code == 400:
            return r.json(), r.status_code
        json_data = r.json()
        new_user_data = json_data['data']
        json_data['data'] = user_schema.dump(new_user_data)
        return json_data, r.status_code


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
