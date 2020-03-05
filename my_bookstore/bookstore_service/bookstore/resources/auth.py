# -*- coding: utf-8 -*-

"""
Authentication-related RESTful API module.
"""

import requests
from flask import g, request
from flask_restful import Resource

from .. import auth


class UserList(Resource):
    """
    Resource for a collection of users.
    """

    def post(self):
        """
        Adds a new user.
        :return:
        """
        # "redirect()" cannot redirect "POST" requests, so we need to manually
        # do the redirecting.
        r = requests.post(
            'http://auth_service:8000/users', json=request.get_json()
        )
        return r.json(), r.status_code


class Token(Resource):
    """
    Resource for token.
    """
    decorators = [auth.login_required]

    def get(self):
        """
        Gets a token for the current logged-in user.
        :return:
        """
        # Even though "redirect()" is able to redirect "GET" requests, it cannot
        # carry data with the redirect, so we need to manually do the
        # redirecting.

        # After logging-in, we can access the username with "g.username"
        r = requests.get(
            'http://auth_service:8000/token', json={'username': g.username}
        )
        return r.json(), r.status_code
