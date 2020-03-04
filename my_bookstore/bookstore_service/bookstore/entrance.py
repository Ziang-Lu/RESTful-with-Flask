# -*- coding: utf-8 -*-

"""
API entrance module.
"""

from typing import List

from flask import Blueprint, url_for
from flask_limiter.util import get_remote_address

from . import limiter
from .utils import RATELIMIT_DEFAULT

entrance_bp = Blueprint(name='entrance', import_name=__name__)


@entrance_bp.route('/')
@entrance_bp.route('/entrance')
@limiter.limit(RATELIMIT_DEFAULT, key_func=get_remote_address)  # This rate-liminting key-function falls back to the default.
def home():
    """
    API entrance.
    :return:
    """
    return {
        'home': _make_entry('entrance.home', allowed_methods=['GET']),
        'add_user': _make_entry('api.add_user', allowed_methods=['POST']),
        'get_token': _make_entry(
            'api.token', allowed_methods=['GET'], require_login=True
        ),
        'authors': _make_entry(
            'api.authors', allowed_methods=['GET', 'POST'], require_login=True
        ),
        'books': _make_entry(
            'api.books', allowed_methods=['GET', 'POST'], require_login=True
        )
    }


def _make_entry(endpoint: str, allowed_methods: List[str],
                require_login: bool=False) -> dict:
    """
    Private helper function to make a entry.
    :param endpoint: str
    :param allowed_methods: list[str]
    :param require_login: bool
    :return: dict
    """
    return {
        'url': url_for(endpoint, _external=True),
        'allowed_methods': allowed_methods,
        'require_login': require_login
    }
