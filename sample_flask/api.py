from flask import Blueprint
from flask_restful import Api

from sample_flask.resources.author import AuthorList, AuthorItem
from sample_flask.resources.book import BookList, BookItem
from sample_flask.resources.auth import Token, UserItem

# Create a API-related blueprint
api_bp = Blueprint(name='api_bp', import_name=__name__)

api = Api(api_bp)
api.add_resource(AuthorList, '/authors')
api.add_resource(AuthorItem, '/authors/<int:id>')
api.add_resource(BookList, '/books')
api.add_resource(BookItem, '/books/<int:id>')
api.add_resource(UserItem, '/users')
api.add_resource(Token, '/token')
