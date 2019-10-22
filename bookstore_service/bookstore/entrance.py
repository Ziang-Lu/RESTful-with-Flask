# -*- coding: utf-8 -*-

"""
API entrance module.
"""

from typing import List

from flask import Blueprint, url_for
from flask_limiter.util import get_remote_address

from . import URL_PREFIX_V1, limiter

entrance_bp = Blueprint(import_name=__name__, url_prefix=URL_PREFIX_V1)


@entrance_bp.route('/', endpoint='entrance')
@limiter.limit(key_func=get_remote_address)
def home():
    """
    API entrance.
    :return:
    """
    return {
        'home': _make_entry('entrance', methods=['GET']),
        'add_user': _make_entry('add_user', methods=['POST']),
        'get_token': _make_entry('token', methods=['GET'], require_login=True),
        'authors': _make_entry(
            'authors', methods=['GET', 'POST'], require_login=True
        ),
        'books': _make_entry(
            'books', methods=['GET', 'POST'], require_login=True
        )
    }


def _make_entry(endpoint: str, methods: List[str],
                require_login: bool=False) -> dict:
    """
    Helper function to make a entry.
    :param endpoint: str
    :param methods: list[str]
    :param require_login: bool
    :return: dict
    """
    return {
        'url': url_for(endpoint, _external=True),
        'methods': methods,
        'require_login': require_login
    }
