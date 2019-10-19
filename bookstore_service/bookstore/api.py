# -*- coding: utf-8 -*-

"""
API defintion module.
"""

from flask import Blueprint
from flask_restful import Api

from .resources.auth import Token, UserItem
from .resources.author import AuthorItem, AuthorList
from .resources.book import BookItem, BookList

# Create a API-related blueprint
api_bp = Blueprint(name='api', import_name=__name__)

api = Api(api_bp)
api.add_resource(AuthorList, '/authors', endpoint='authors')
api.add_resource(AuthorItem, '/authors/<int:id>', endpoint='author')
api.add_resource(BookList, '/books', endpoint='books')
api.add_resource(BookItem, '/books/<int:id>', endpoint='book')
api.add_resource(UserItem, '/users')
api.add_resource(Token, '/token')
