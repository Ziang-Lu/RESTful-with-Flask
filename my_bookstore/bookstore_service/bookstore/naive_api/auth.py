# -*- coding: utf-8 -*-

"""
Authentication-related RESTful API module.
"""

import requests
from flask import Blueprint, g, request
from flask_limiter.util import get_remote_address
from marshmallow import ValidationError

from .. import auth, limiter
from ..models import user_schema
from ..utils import RATELIMIT_NORMAL, RATELIMIT_SLOW

auth_bp = Blueprint(name='auth', import_name=__name__)


@auth_bp.route('/users', methods=['POST'])
@limiter.limit(RATELIMIT_NORMAL, key_func=get_remote_address)  # For this route, since we don't do authentication, we need to use the remote address as the rate-limiting key.
def add_user():
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


@auth_bp.route('/token')
@auth.login_required
@limiter.limit(RATELIMIT_SLOW)
def get_token():
    """
    Gets a token for the current logged-in user.
    :return:
    """
    # After logging-in, we can access the username with "g.username"
    r = requests.get(
        'http://auth_service:8000/token', json={'username': g.username}
    )
    return r.json(), r.status_code
