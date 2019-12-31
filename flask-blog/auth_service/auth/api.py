# -*- coding: utf-8 -*-

"""
API definition module.
"""

from flask import Blueprint
from flask_restful import Api

from .resources.auth import Token, UserAuth, UserList

# Create an API-related blueprint
api_bp = Blueprint(name='api', import_name=__name__)

api = Api(api_bp)
api.add_resource(UserList, '/users')
api.add_resource(UserAuth, '/user-auth')
api.add_resource(Token, '/token')
