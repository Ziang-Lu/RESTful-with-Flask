# -*- coding: utf-8 -*-

"""
API definition module.
"""

from flask import Blueprint
from flask_restful import Api

from .resources.auth import Token, UserItem, UserAuth

# Create a API-related blueprint
api_bp = Blueprint(name='api', import_name=__name__)

api = Api(api_bp)
api.add_resource(UserItem, '/users')
api.add_resource(UserAuth, '/user-auth')
api.add_resource(Token, '/token')
