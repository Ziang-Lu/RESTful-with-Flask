# -*- coding: utf-8 -*-

"""
Authentication-related RESTful API module.
"""

from flask import Blueprint, g, request
from flask_limiter.util import get_remote_address
from marshmallow import ValidationError

from .. import URL_PREFIX_V1, auth, bcrypt, db, limiter
from ..models import User, user_schema
from ..utils import RATELIMIT_NORMAL, RATELIMIT_SLOW

auth_bp = Blueprint(name='auth', import_name=__name__, url_prefix=URL_PREFIX_V1)


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

    if User.query.filter_by(username=user_data['username']).first():
        return {
            'status': 'error',
            'message': 'User already exist'
        }, 400

    username, password = user_data['username'], user_data['password']
    new_user = User(
        username=username,
        password=bcrypt.generate_password_hash(password).decode('utf-8')
    )
    db.session.add(new_user)
    db.session.commit()
    return {
        'status': 'success',
        'data': user_schema.dump(new_user)
    }, 201


@auth_bp.route('/token')
@auth.login_required
@limiter.limit(RATELIMIT_SLOW)
def get_token():
    """
    Gets a token for the current logged-in user.
    :return:
    """
    # After logging in, we can access the user with "g.user"
    token, duration = g.user.generate_token()
    return {
        'token': token.decode('ascii'),
        'duration in seconds': duration
    }
